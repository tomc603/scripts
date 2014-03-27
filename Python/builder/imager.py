#!/usr/bin/python2.7

__author__ = 'tcameron'


class Bootstrap:
    _depends = ['debootstrap', ]
    _staging = ''
    _arch = 'amd64'
    _distro = ''
    _pkgmanager = None
    _pkgmirror = 'http://archive.ubuntu.com/ubuntu'
    _setup = ''

    def __init__(self, staging, arch, distribution, manager, mirror, image):
        # Set up class variables
        self._staging = staging
        self._arch = arch
        self._distro = distribution
        self._pkgmanager = manager
        self._pkgmirror = mirror
        self._depends += image.getdepends()

    def _mountdev(self):
        # Mount self.staging/dev
        return True

    def _mountdevpts(self):
        # Mount self.staging/dev/pts
        return True

    def _mountproc(self):
        # Mount self.staging/proc
        return True

    def _mountsys(self):
        # Mount self.staging/sys
        return True

    def checkdepends(self):
        self._pkgmanager.checkpackages(self._depends)
        return True

    def installdepends(self):
        return True

    def domounts(self):
        self._mountproc()
        self._mountsys()
        self._mountdev()
        self._mountdevpts()

    def updaterepo(self):
        # Execute packaging repository update process
        return True

    def upgradepkgs(self):
        # Execute package update process
        return True


class Origin:
    _srcpath = ''

    def __init__(self, path):
        self._srcpath = path


class Image:
    _depends = []
    _cmd = ''

    def __init__(self):
        pass

    def getdepends(self):
        return self._depends


if __name__ == "__main__":
    pass
