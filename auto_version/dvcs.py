"""
auto_version.dvcs
~~~~~~~~~~~~~~~~~

This modules contains all the implementation for versionning system automation.

see `Issue#1 <https://github.com/paulollivier/auto_versionning/issues/1>`_

The resulting version number will be in the form `<ChosenStyle>+<VCSStyle>`.

For git, VCSStyle is in the form `pre<number_of_commits_since_last_tag>-<sha_hash_of_last_commit>-<is_dirty?>`

If the user wants to use DVCS system, the option --use-vcs should be present, or "use_vcs": True should be present in config. This way, people won't find creepy hashes in their version string.
"""

import os
from subprocess import check_output, check_call, CalledProcessError
from auto_version.utils import logger


class BaseVCS:
    """
    Base VCS class

    .. attention::

        Do not use, use the actual vcs implementations instead
    """

    __meta_dir__ = ".meta"  # Should be overriden to reflect the meta-information folder for each system.

    def __init__(self):
        self.meta_info_present = self.__meta_dir__ in os.listdir(os.path.abspath('.'))

    def get_status(self):
        """
        Returns the `status` of the repository
        """
        raise NotImplementedError("This versionning class is not designed to be used, but rather as a base for actual implementations to rely on.")

    def get_current_version(self, with_status=False):
        """
        Return the current version, from the state of the repository.
        """
        raise NotImplementedError("This versionning class is not designed to be used, but rather as a base for actual implementations to rely on.")

    def set_version(self, version=None):
        """
        When a verison increment is made, update the vcs
        """
        raise NotImplementedError("This versionning class is not designed to be used, but rather as a base for actual implementations to rely on.")


class Git(BaseVCS):
    """
    Provides git support, via git tags. As many tag their commits with release numbers, it is a good idea to sync auto-version with these tags.

    .. warning:

        for now, self.style must be set after instanciation, before any call to the instance
    """

    __meta_dir__ = ".git"

    def __init__(self):
        self.status = None
        BaseVCS.__init__(self)

    def _update_index(self):
        """
        Updates the git index.
        """
        try:
            check_output(["git", "update-index", "--refresh", "-q"])  # Silencing output of git update-index
        except CalledProcessError:
            pass

    def _get_describe(self, increment=True):
        s = check_output(["git", "describe", "--tags", "--dirty"])  # TODO: actually, we force users to use vX.X(...) tags. find an other way. This is a bit unsafe.
        logger.debug(str(type(s)) + " " + s)
        self.status = [str(s) for s in s.strip('\n').split('-')]  # check_output returns bytes
        logger.debug("self.status = " + str(self.status))
        if(len(self.status) > 1 and self.status[1] != "dirty" and increment):
            logger.debug(self.status[0])
            self.status[0] = self.style(
                self.style.get_pure_version_string(
                    self.style,
                    self.status[0]
                    )
                ).increment()
        else:
            self.status[0] = self.style.get_pure_version_string(
                self.style,
                self.status[0]
                )

        return self.status

    def get_status(self):
        self._update_index()
        if(self.status is None):
            logger.debug("Self.status is None. Updating... result:" + self._get_describe())
        logger.debug("self.status is %d long" % len(self.status))
        if(len(self.status) >= 3):
            logger.debug(self.status[1:])
            return "-pre%s-%s" % (self.status[1], self.status[2])
        else:
            return ""

    def get_current_version(self, with_status=False, increment=True):
        self._update_index()
        logger.debug(self._get_describe(increment=increment))
        if(with_status):
            logger.info("".join((self.status[0], self.get_status())))
            return "".join((self.status[0], self.get_status()))
        return self.status[0]

    def set_version(self, version=None, prefix=""):
        if(version):
            check_call(["git", "tag", prefix + version])