from llnl.util.filesystem import LibraryList
from spack import *

class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "https://www.olcf.ornl.gov/software_package/libsci/"
    url      = "https://www.olcf.ornl.gov/software_package/libsci/"

    version("16.11.1")
    version("16.06.1")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    # NOTE: Cray compiler wrappers already include linking for the following
    @property
    def blas_libs(self):
        return LibraryList([self.prefix.lib])

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    def install(self, spec, prefix):
        raise NoBuildError(spec)
