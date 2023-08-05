from setux.core.manage import Manager


class Distro(Manager):
    manager = 'os'

    @property
    def kernel(self):
        ret, out, err = self.run('uname -s')
        return out[0]

    @property
    def version(self):
        ret, out, err = self.run('uname -r')
        return out[0].split('-')[0]

    @property
    def arch(self):
        ret, out, err = self.run('uname -m')
        return out[0]
