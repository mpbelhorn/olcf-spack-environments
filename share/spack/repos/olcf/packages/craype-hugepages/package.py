from spack import *

class CraypeHugepages(Package):
    """CrayPE-hugepages implementation."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/craype-hugepages-8M.tar.gz"

    version('8M', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        raise InstallError('CrayPE Hugepages is not installable; it is vendor supplied')
