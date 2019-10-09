from spack import *

class Hsi(Package):
    """Description"""

    homepage = "file://sw/sources/hpss"
    url = "https://github.com/robertdfrench/empty.git"

    version('olcf', git="https://github.com/robertdfrench/empty.git")
    version('ncrc', git="https://github.com/robertdfrench/empty.git")

    def install(self, spec, prefix):
      mkdirp(prefix.bin)
      mkdirp(prefix.man)
      ln = which('ln')
      if str(spec.version) == 'olcf':
        ln('-s', '/sw/sources/hpss/bin/hsi', prefix.bin+'/hsi')
        ln('-s', '/sw/sources/hpss/bin/htar', prefix.bin+'/htar')
        ln('-s', '/sw/sources/hpss/man/man1', prefix.man+'/man1')
      elif str(spec.version) == 'ncrc':
        ln('-s', '/sw/rdtn/hsi/default/bin/hsi', prefix.bin+'/hsi')
        ln('-s', '/sw/rdtn/htar/default/bin/htar', prefix.bin+'/htar')
