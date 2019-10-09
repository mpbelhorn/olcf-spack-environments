from spack import *

class CrayMpich(Package):
    """Cray MPI implementation."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/cray-mpich-7.4.0.tar.gz"

    version('7.4.0', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    def install(self, spec, prefix):
        raise InstallError('Cray MPICH is not installable; it is vendor supplied')

    def setup_dependent_package(self, module, dspec):
        # Spack wrappers call the Cray wrappers.
        self.spec.mpicc = spack_cc
        self.spec.mpicxx = spack_cxx
        self.spec.mpif77 = spack_f77
        self.spec.mpif90 = spack_fc
        self.spec.mpifc = spack_fc
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpichcxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpich.{0}'.format(dso_suffix))
        ]

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  spack_cc)
        spack_env.set('MPICXX', spack_cxx)
        spack_env.set('MPIF77', spack_f77)
        spack_env.set('MPIF90', spack_fc)
