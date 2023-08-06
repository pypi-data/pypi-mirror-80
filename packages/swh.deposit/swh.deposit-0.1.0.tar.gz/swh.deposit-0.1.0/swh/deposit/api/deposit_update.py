# Copyright (C) 2017-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Any, Dict, Optional, Tuple

from rest_framework import status

from ..config import CONT_FILE_IRI, EDIT_SE_IRI, EM_IRI
from ..errors import BAD_REQUEST, make_error_dict
from ..parsers import (
    SWHAtomEntryParser,
    SWHFileUploadTarParser,
    SWHFileUploadZipParser,
    SWHMultiPartParser,
)
from .common import ACCEPT_ARCHIVE_CONTENT_TYPES, APIDelete, APIPost, APIPut


class APIUpdateArchive(APIPost, APIPut, APIDelete):
    """Deposit request class defining api endpoints for sword deposit.

       What's known as 'EM IRI' in the sword specification.

       HTTP verbs supported: PUT, POST, DELETE

    """

    parser_classes = (
        SWHFileUploadZipParser,
        SWHFileUploadTarParser,
    )

    def process_put(
        self, req, headers, collection_name: str, deposit_id: int
    ) -> Dict[str, Any]:
        """Replace existing content for the existing deposit.

           source: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_editingcontent_binary  # noqa

        Returns:
            204 No content

        """
        if req.content_type not in ACCEPT_ARCHIVE_CONTENT_TYPES:
            msg = "Packaging format supported is restricted to %s" % (
                ", ".join(ACCEPT_ARCHIVE_CONTENT_TYPES)
            )
            return make_error_dict(BAD_REQUEST, msg)

        return self._binary_upload(
            req, headers, collection_name, deposit_id=deposit_id, replace_archives=True
        )

    def process_post(
        self, req, headers: Dict, collection_name: str, deposit_id: Optional[int] = None
    ) -> Tuple[int, str, Dict]:
        """Add new content to the existing deposit.

           source: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_addingcontent_mediaresource  # noqa

        Returns:
            201 Created
            Headers: Location: [Cont-File-IRI]

            Body: [optional Deposit Receipt]

        """
        if req.content_type not in ACCEPT_ARCHIVE_CONTENT_TYPES:
            msg = "Packaging format supported is restricted to %s" % (
                ", ".join(ACCEPT_ARCHIVE_CONTENT_TYPES)
            )
            unused = 0
            return unused, "unused", make_error_dict(BAD_REQUEST, msg)

        return (
            status.HTTP_201_CREATED,
            CONT_FILE_IRI,
            self._binary_upload(req, headers, collection_name, deposit_id),
        )

    def process_delete(self, req, collection_name: str, deposit_id: int) -> Dict:
        """Delete content (archives) from existing deposit.

           source: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_deletingcontent  # noqa

        Returns:
            204 Created

        """
        return self._delete_archives(collection_name, deposit_id)


class APIUpdateMetadata(APIPost, APIPut, APIDelete):
    """Deposit request class defining api endpoints for sword deposit.

       What's known as 'Edit IRI' (and SE IRI) in the sword specification.

       HTTP verbs supported: POST (SE IRI), PUT (Edit IRI), DELETE

    """

    parser_classes = (SWHMultiPartParser, SWHAtomEntryParser)

    def process_put(
        self, req, headers: Dict, collection_name: str, deposit_id: int
    ) -> Dict[str, Any]:
        """Replace existing deposit's metadata/archive with new ones.

           source:
           - http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_editingcontent_metadata  # noqa
           - http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_editingcontent_multipart  # noqa

        Returns:
            204 No content

        """
        if req.content_type.startswith("multipart/"):
            return self._multipart_upload(
                req,
                headers,
                collection_name,
                deposit_id=deposit_id,
                replace_archives=True,
                replace_metadata=True,
            )
        return self._atom_entry(
            req, headers, collection_name, deposit_id=deposit_id, replace_metadata=True
        )

    def process_post(
        self,
        request,
        headers: Dict,
        collection_name: str,
        deposit_id: Optional[int] = None,
    ) -> Tuple[int, str, Dict]:
        """Add new metadata/archive to existing deposit.

           source:
           - http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_addingcontent_metadata  # noqa
           - http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_addingcontent_multipart  # noqa

        This also deals with an empty post corner case to finalize a
        deposit.

        Returns:
            In optimal case for a multipart and atom-entry update, a
            201 Created response. The body response will hold a
            deposit. And the response headers will contain an entry
            'Location' with the EM-IRI.

            For the empty post case, this returns a 200.

        """
        assert deposit_id is not None
        if request.content_type.startswith("multipart/"):
            return (
                status.HTTP_201_CREATED,
                EM_IRI,
                self._multipart_upload(
                    request, headers, collection_name, deposit_id=deposit_id
                ),
            )
        # check for final empty post
        # source: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html
        # #continueddeposit_complete
        if headers["content-length"] == 0 and headers["in-progress"] is False:
            data = self._empty_post(request, headers, collection_name, deposit_id)
            return (status.HTTP_200_OK, EDIT_SE_IRI, data)

        return (
            status.HTTP_201_CREATED,
            EM_IRI,
            self._atom_entry(request, headers, collection_name, deposit_id=deposit_id),
        )

    def process_delete(self, req, collection_name: str, deposit_id: int) -> Dict:
        """Delete the container (deposit).

           source: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_deleteconteiner  # noqa

        """
        return self._delete_deposit(collection_name, deposit_id)
