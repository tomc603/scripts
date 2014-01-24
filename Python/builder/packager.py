__author__ = 'tcameron'

class Rpm:
    _pkgcmd = 'yum'
    _updatecmd = ''
    _upgradecmd = ''
    _installcmd = ''
    _uninstallcmd = ''

    def __init__(self):
        pass

    def _status(self, name):
        return True

    def update(self):
        return True

    def upgrade(self):
        return True

    def install(self, packages):
        return True

    def uninstall(self, packages):
        return True

    def checkpackages(self, packagelist):
        for pkg in packagelist:
            print('Checking: %s' % pkg)
            if not self._status(pkg):
                return False
        return True


class Dpkg:
    _pkgcmd = 'apt-get'
    _updatecmd = 'update'
    _upgradecmd = 'upgrade'
    _installcmd = 'install'
    _uninstallcmd = 'remove'


    def __init__(self):
        pass

    def _status(self, name):
        return True

    def update(self):
        return True

    def upgrade(self):
        return True

    def install(self, packages):
        return True

    def uninstall(self, packages):
        return True

    def checkpackages(self, packagelist):
        for pkg in packagelist:
            print('Checking: %s' % pkg)
            if not self._status(pkg):
                return False
        return True
