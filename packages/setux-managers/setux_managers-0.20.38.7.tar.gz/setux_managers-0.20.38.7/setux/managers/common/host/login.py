from setux.core.manage import Manager


class Distro(Manager):
    manager = 'login'

    @property
    def name(self):
        ret, out, err = self.run('id -un')
        return out[0]

    @property
    def id(self):
        ret, out, err = self.run('id -u')
        return int(out[0])
