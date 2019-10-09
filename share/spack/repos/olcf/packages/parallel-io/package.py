##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################


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
 
    version('2.3.0', 'e1d89747130702a81dbc425b08b75ef9')
    version('2.2.2', '7040b864ccc693e806f2bf07659aa080')
    version('2.2.0', '43297a4aaa034a7d0c70452fcd999a00')

    depends_on('mpi')
    depends_on('netcdf+mpi+parallel-netcdf')
    depends_on('netcdf-fortran')
    depends_on('parallel-netcdf+pic')

    def url_for_version(self, version):
        base_url = "https://github.com/NCAR/ParallelIO/archive"
        return "{0}/pio{1}.tar.gz".format(base_url, version.underscored)

    def cmake_args(self):
        spec = self.spec
        args = []

        args.extend([
            '-DCMAKE_C_COMPILER:FILEPATH=%s' % spec['mpi'].mpicc,
            '-DCMAKE_Fortran_COMPILER:FILEPATH=%s' % spec['mpi'].mpifc,
            '-DCMAKE_C_STANDARD:STRING=99',
            ])

        if spec.satisfies('%xl'):
            args.extend([
                '-DCMAKE_C_COMPILER_ID=XL',
                # The examples have some issues with XL, so skip them for this
                # compiler.
                '-DPIO_ENABLE_EXAMPLES:BOOL=OFF',
                ])

        args.extend([
            '-DNetCDF_C_PATH:FILEPATH=%s' % spec['netcdf'].prefix,
            '-DNetCDF_Fortran_PATH:FILEPATH=%s' % spec['netcdf-fortran'].prefix,
            '-DPnetCDF_PATH:FILEPATH=%s' % spec['parallel-netcdf'].prefix,
            ])

        return args
