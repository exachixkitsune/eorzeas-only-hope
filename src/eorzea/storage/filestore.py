#!/usr/bin/python3
# vim: ts=4 expandtab

"""A data store of names of people who can save Eorzea, written to a file
with one entry per line"""

from __future__ import annotations

from typing import Any, Optional, Set, TextIO
from os.path import exists as path_exists

from .datastore import DataStore, RaiseType


class FileStore(DataStore):
    """A data store of names of people who can save Eorzea, written to a file
    with one entry per line"""

    file_handle: TextIO

    def __init__(self: FileStore, file_name: str):
        """Sets up the data store, reading the data set
        from the file if needed"""

        from_storage: Optional[Set[str]] = None

        if path_exists(file_name):
            with open(file_name) as handle:
                from_storage = {line.strip() for line in handle}

        super().__init__(from_storage)

        self.file_handle = open(file_name, "a")

    def _write_append(self: FileStore, value: str) -> Optional[bool]:
        """Append a value to the underlying data store this type implements.

        This function may be a no-op method, in which case it MUST return None.
        Otherwise, it should return if the write succeeded.

        Values passed to this function SHOULD NOT exist in the store already,
        so the implement does not need to consider de-duplication.
        """
        return self.file_handle.write("%s\n" % value) > 0

    def _write_list(self: FileStore, value: Set[str]) -> Optional[bool]:
        return None

    def __exit__(
        self: FileStore, exception_type: RaiseType, message: Any, traceback: Any
    ) -> Optional[bool]:
        self.file_handle.close()

        return super().__exit__(exception_type, message, traceback)
