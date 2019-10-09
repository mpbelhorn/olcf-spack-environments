# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Ferret(MakefilePackage):
    """Ferret is an interactive computer visualization and analysis environment
       designed to meet the needs of oceanographers and meteorologists
       analyzing large and complex gridded data sets."""
    homepage = "http://ferret.pmel.noaa.gov/Ferret/home"
    url      = "https://github.com/NOAA-PMEL/Ferret/archive/7.4.4.tar.gz"

    version('7.4.4', '7d18b906e4f1a0f6401d2f765ce3013c573e69ecd346167ac8af1e5cc5e3f2f7')

    depends_on("hdf5~mpi+fortran+szip")
    depends_on("netcdf~mpi")
    depends_on("netcdf-fortran")
    depends_on("readline")

    parallel = False

    def edit(self, spec, prefix):
        ssmk_target = join_path(self.stage.source_path, 'site_specific.mk')
        copy(ssmk_target + '.in', ssmk_target)
        site_specific = FileFilter(ssmk_target)
        site_specific.filter('DIR_PREFIX = .*',
                             'DIR_PREFIX = ' + self.stage.source_path)
        site_specific.filter('BUILDTYPE = .*',
                             'BUILDTYPE = x86_64-linux')
        site_specific.filter('INSTALL_FER_DIR = .*',
                             'INSTALL_FER_DIR = %s' % self.prefix)
        site_specific.filter('HDF5_LIBDIR = .*', 'HDF5_LIBDIR = ')
                             # 'HDF5_LIBDIR = %s' % spec['hdf5'].prefix.lib)
        site_specific.filter('NETCDF_LIBDIR = .*', 'NETCDF_LIBDIR = %s' % spec['netcdf'].prefix.lib)
        site_specific.filter('READLINE_LIBDIR = .*', 'READLINE_LIBDIR = ')
                             # 'READLINE_LIBDIR = %s' % spec['readline'].prefix.lib)

        ef_ssmk_target = join_path(
            self.stage.source_path,
           'external_functions/ef_utility/site_specific.mk')
        copy(ef_ssmk_target + '.in', ef_ssmk_target)
        ext_site_specific = FileFilter(ef_ssmk_target)
        ext_site_specific.filter('BUILDTYPE = .*', 'BUILDTYPE = x86_64-linux')

        platform = FileFilter('platform_specific.mk.x86_64-linux')
        platform.filter('\tMYINCLUDES\t=.*', '\tMYINCLUDES\t= -I. -I%s \\' % spec['netcdf-fortran'].prefix.include)
        platform.filter('\t\t\t  -lnetcdff.*', '\t\t\t  -L%s -lnetcdff \\' % spec['netcdf-fortran'].prefix.lib)
        platform.filter('\tCC\t\t=.*', '\tCC\t\t= %s' % spack_cc)
        platform.filter('\tFC\t\t=.*', '\tFC\t\t= %s' % spack_fc)
        platform.filter('\tF77\t\t=.*', '\tFC\t\t= %s' % spack_fc)
        platform.filter('\tLD\t\t=.*', '\tLD\t\t= %s' % spack_fc)
        platform.filter('\tLDFLAGS\t\t=.*', '\tLDFLAGS\t\t= -m64 -L/lib64 -L/lib -lgfortran -export-dynamic')
