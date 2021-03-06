# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nco(AutotoolsPackage):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "http://nco.sourceforge.net/"
    url      = "https://github.com/nco/nco/archive/4.6.7.tar.gz"

    version('4.9.1', 'eb1a00cceb0509f856fd5011ef9ea4d4')
    version('4.8.1', '547209b355cc20b87f6e093fbf810557')
    version('4.6.9', 'e7fa2b6d62d1eb34b721160f4e35caa2')
    version('4.6.7', 'b04c92aa715d3fad3ebebd1fd178ce32')
    version('4.6.6', 'df6fa47aaf6e41adfc0631912a7a341f')
    version('4.6.5', '2afd34a6bb5ff6c7ed39cf40c917b6e4')
    version('4.6.4', '22f4e779d0011a9c0db90fda416c8e45')
    version('4.6.3', '0e1d6616c65ed3a30c54cc776da4f987')
    version('4.6.2', 'b7471acf0cc100343392f4171fb56113')
    version('4.6.1', 'ef43cc989229c2790a9094bd84728fd8')
    version('4.5.5', '9f1f1cb149ad6407c5a03c20122223ce')


    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld
    variant('mpi-deps', default=True,
            description='Build NCO against MPI-enabled dependencies')
    variant('mpi', default=False,
            description='Build MPI-enabled NCO (not recommended)')
    variant('ncap2', default=True,
            description='Build ncap2 and libnco++')
    variant('doc', default=True,
            description='Build/install NCO TexInfo-based documentation')

    depends_on('netcdf-c~mpi~parallel-netcdf', when='~mpi-deps')
    depends_on('netcdf-c+mpi+parallel-netcdf', when='+mpi-deps')
    depends_on('hdf5~mpi', type=('run',), when='~mpi-deps')
    depends_on('hdf5+mpi', type=('run',), when='+mpi-deps')
    depends_on('mpi', when='+mpi')
    depends_on('antlr@2.7.7+cxx', when='+ncap2')
    depends_on('gsl') # desirable for ncap2
    depends_on('udunits') # allows dimensional unit transformations

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('texinfo@4.12:', type='build', when='+doc')

    conflicts('~mpi-deps', when='+mpi')

    def patch(self):
        """NULL-0-NULL patch."""
        # https://github.com/nco/nco/issues/43
        if self.spec.satisfies('@:4.6.7'):
            filter_file(r"char \*pend='\\0';",
                        "char *pend=NULL;",
                        "src/nco++/fmc_all_cls.cc")

    def configure_args(self):
        spec = self.spec
        opts = ['--{0}-doc'.format('enable' if spec.satisfies('+doc') else 'disable')]
        opts = ['--{0}-mpi'.format('enable' if spec.satisfies('+mpi') else 'disable')]

        if '+ncap2' in spec:
            opts.append('--enable-ncap2')
        else:
            opts.append('--disable-ncap2')
        return opts

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        spack_env.set('NETCDF_INC', spec['netcdf-c'].prefix.include)
        spack_env.set('NETCDF_LIB', spec['netcdf-c'].prefix.lib)
        spack_env.set('UDUNITS2_PATH', spec['udunits'].prefix)
        if self.spec.satisfies('+ncap2'):
            spack_env.set('ANTLR_ROOT', spec['antlr'].prefix)
