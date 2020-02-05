# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class ParallelIo(CMakePackage):
    """The Parallel I/O (PIO) library has been developed over several years to
    improve the ability of component models of the Community Earth System Model
    (CESM) to perform I/O. The focus of development has been on backend tools
    that use the NetCDF file format. PIO currently supports NetCDF and PnetCDF
    as backend libraries, both can be linked and used with runtime options
    controlling which is used for a given file.
    
    PIO2 represents a significant rewrite of the PIO library and includes a C
    API as well as the original F90 API. A new decomposition strategy has been
    introduced which gives the user more ability to tune io communications.
    """

    homepage = "http://ncar.github.io/ParallelIO"
    url      = "https://github.com/NCAR/ParallelIO/archive/pio2_2_0.tar.gz"
 
    version('2.4.4', 'd72a431c6ce07201ae7b1a52f7af054b')
    version('2.3.0', 'e1d89747130702a81dbc425b08b75ef9')
    version('2.2.2', '7040b864ccc693e806f2bf07659aa080')
    version('2.2.0', '43297a4aaa034a7d0c70452fcd999a00')

    variant('examples', default=False, description='Builds the examples')

    depends_on('mpi')
    depends_on('netcdf-c+mpi+parallel-netcdf')
    depends_on('netcdf-fortran+pic')
    depends_on('parallel-netcdf+pic+fortran')
    depends_on('hdf5+fortran+mpi')
    depends_on('zlib')

    # The examples have issues with XL
    conflicts('+examples', when='@:2.3.0%xl')
    conflicts('+examples', when='@:2.3.0%xl_r')


    def url_for_version(self, version):
        base_url = "https://github.com/NCAR/ParallelIO/archive"
        return "{0}/pio{1}.tar.gz".format(base_url, version.underscored)

    def cmake_args(self):
        spec = self.spec
        args = []

        args.extend([
            '-DCMAKE_C_COMPILER:FILEPATH=%s' % spec['mpi'].mpicc,
            '-DCMAKE_Fortran_COMPILER:FILEPATH=%s' % spec['mpi'].mpifc,
            # '-DCMAKE_C_STANDARD:STRING=99',
            '-DNetCDF_C_PATH:FILEPATH=%s' % spec['netcdf-c'].prefix,
            '-DNetCDF_Fortran_PATH:FILEPATH=%s' % spec['netcdf-fortran'].prefix,
            '-DPnetCDF_PATH:FILEPATH=%s' % spec['parallel-netcdf'].prefix,
            '-DHDF5_PATH=%s' % spec['hdf5'].prefix,
            '-DLIBZ_PATH=%s' % spec['zlib'].prefix,
            ])

        if spec.satisfies('~examples'):
            args.append('-DPIO_ENABLE_EXAMPLES:BOOL=OFF')

        if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
            args.extend([
                '-DCMAKE_C_COMPILER_ID=XL',
                ])

        return args
