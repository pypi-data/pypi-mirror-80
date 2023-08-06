"""Declares :class:`LocalDiskBackend`."""
import shutil
import os

from .base import BaseStorageBackend


class LocalDiskBackend(BaseStorageBackend):
    """A storage backend that uses the local filesystem."""
    kind = 'local'

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        handler.fd.close()

    def download(self, path, dst):
        """This method exists only for API compatibility."""
        shutil.copy2(self.storage_path(path), dst)
        return dst

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return os.path.exists(self.storage_path(path))

    def get_local_fd(self, handler):
        """Opens a local file descriptor."""
        local_path = self.storage_path(handler.path)
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        return open(local_path, handler.mode)

    def update_labels(self, labels): # pylint: disable=W0107
        """Update dictionary `labels` with the label for a specific
        storage backend.
        """

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        return handler.fd.read(size)

    def push(self, src, path):
        """Copies local absolute path `src` to remote `path`."""
        dst = self.storage_path(path)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy2(src, dst)

    def unlink(self, path):
        """Remove a path."""
        dst = self.storage_path(path)
        if os.path.isdir(dst):
            func = shutil.rmtree
        else:
            func = os.unlink
        func(dst)


StorageBackend = LocalDiskBackend
