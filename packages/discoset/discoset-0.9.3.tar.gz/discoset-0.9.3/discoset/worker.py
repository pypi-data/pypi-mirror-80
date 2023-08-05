import logging
import stat
from dataclasses import dataclass
from pathlib import Path

from .config import Item

logger = logging.getLogger()


class Worker:
    """Create all the items

    We blatantly assume that between calls to is_valid() and execute() the
    state of the filesystem does not change. This assumption might not hold
    at all times - but for our purposes, this can be ignored.
    """

    def __init__(self, source_directory, target_directory, items):
        self.source_directory = source_directory
        self.target_directory = target_directory

        # Convert items to absolute paths
        self.items = [
            Item(
                target=(self.target_directory / i.target),
                source=(self.source_directory / i.source),
                permissions=i.permissions,
            )
            for i in items
        ]
        self.warnings = []
        self.errors = []
        self._operations = []

    def is_valid(self):
        """
        Following possibilities:

            * Target file does not exist.

            * Target file exists, but is a link into the current
              discoset directory, and the link target is up-to-date.

            * Target file exists, but is a link into the current
              discoset directory and the link target is NOT up-to-date.

            * Target file exists, but is an alien file
        """
        self._operations.clear()

        for item in self.items:
            if item.target.exists():
                if item.target.is_symlink():
                    resolved = item.target.resolve()
                    # is the symlink pointing to something in our source
                    # directory
                    try:
                        relative = resolved.relative_to(self.source_directory)
                    except ValueError:
                        self.errors.append(f"{item.target} is an alien symlink")
                        break
                    else:
                        if relative != item.source.relative_to(self.source_directory):
                            self.warnings.append(f"{item.target} will be updated")
                            self._operations.append(Unlink(item))
                            self._operations.append(CreateSymlink(item))

                    st_mode = item.target.resolve().stat().st_mode
                    permissions = st_mode & ~(
                        stat.S_IFREG | stat.S_IFLNK | stat.S_IFDIR
                    )
                    if (
                        item.permissions is not None
                        and int(item.permissions, 8) != permissions
                    ):
                        self._operations.append(SetPermissions(item))
                else:
                    self.errors.append(f"{item.target} is an alien file")
                    break
            else:
                # Check if source exists
                if not item.source.exists():
                    self.warnings.append(f"{item.source} does not exist")
                self._operations.append(CreateSymlink(item))
                if item.permissions is not None:
                    self._operations.append(SetPermissions(item))

        return len(self.errors) == 0

    def execute(self):
        """Before calling execute() you must make sure that is_valid() was
        called"""
        assert len(self.errors) == 0
        logger.debug("ops", self._operations)
        for op in self._operations:
            op()
            logger.info("%s", op)


@dataclass
class CreateSymlink:
    item: Item

    def __call__(self):
        target = self.item.target.resolve()
        source = self.item.source.resolve()
        if not target.parent.exists():
            logger.info("Creating dir %s", target.parent)
            target.parent.mkdir(parents=True)
        target.symlink_to(source)

    def __str__(self):
        source = self.item.source.resolve()
        return f"Creating symlink {self.item.target} -> {source}"


@dataclass
class Unlink:
    item: Item

    def __call__(self):
        self.item.target.unlink()

    def __str__(self):
        return f"Removing {self.item.target}"


@dataclass
class SetPermissions:
    item: Item

    def __call__(self):
        self.item.target.resolve().chmod(int(self.item.permissions, 8))

    def __str__(self):
        target = self.item.target.resolve()
        return f"Setting permission of {target} to {self.item.permissions}"
