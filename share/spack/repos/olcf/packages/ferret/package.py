# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/NOAA-PMEL/Ferret/archive/v7.6.0.tar.gz"

    maintainers = ['RemiLacroix-IDRIS', 'mpbelhorn']

    version('7.6.0', sha256='69832d740bd44c9eadd198a5de4d96c4c01ae90ae28c2c3414c1bb9f43e475d1')
    version('7.5.0', sha256='2a038c547e6e80e6bd0645a374c3247360cf8c94ea56f6f3444b533257eb16db')
    version('7.4.4', sha256='7d18b906e4f1a0f6401d2f765ce3013c573e69ecd346167ac8af1e5cc5e3f2f7')

    variant('datasets', default=False, description="Install Ferret standard datasets")

    depends_on("hdf5+hl~mpi+fortran+szip")
    depends_on("netcdf-c~mpi")
    depends_on("netcdf-fortran")

    depends_on("zlib")
    depends_on("curl")
    # depends_on("readline")
    # depends_on("libx11")

    # Make Java dependency optional with older versions of Ferret
    patch('https://github.com/NOAA-PMEL/Ferret/commit/c7eb70a0b17045c8ca7207d586bfea77a5340668.patch',
          sha256='5bd581db4578c013faed375844b206fbe71f93fe9ce60f8f9f41d64abc6a5972',
          level=1, working_dir='FERRET', when='@:6.99')

    resource(name='datasets',
             url='https://github.com/NOAA-PMEL/FerretDatasets/archive/v7.6.tar.gz',
             sha256='b2fef758ec1817c1c19e6225857ca3a82c727d209ed7fd4697d45c5533bb2c72',
             placement='fer_dsets', when='+datasets')

    def url_for_version(self, version):
        if version <= Version('7.2'):
            return 'ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v{0}.tar.gz'.format(
                version.joined)
        else:
            return 'https://github.com/NOAA-PMEL/Ferret/archive/v{0}.tar.gz'.format(version)

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
        site_specific.filter(r'^(NETCDF4?_(LIB)?DIR).+', '\\1 = %s' % spec['netcdf-c'].prefix.lib)
        site_specific.filter(r'^(HDF5_(LIB)?DIR).+', '\\1 = %s' % spec['hdf5'].prefix)
        # Following set to blank in order to pickup dynamic libs
        site_specific.filter(r'^(READLINE_(LIB)?DIR).+', '\\1 = ')

        ef_ssmk_target = join_path(
            self.stage.source_path,
           'external_functions/ef_utility/site_specific.mk')
        copy(ef_ssmk_target + '.in', ef_ssmk_target)
        ext_site_specific = FileFilter(ef_ssmk_target)
        ext_site_specific.filter('BUILDTYPE = .*', 'BUILDTYPE = x86_64-linux')

        # FIXME: improve regex to handle changing tabs and flexibly link correct
        # `NETCDF*_[LIB]DIR`,  `HDF5_[LIB]DIR` paths and libs
        # (-lhdf5_hl, -lhdf5, -lnetrcdff, etc.)
        platform = FileFilter('platform_specific.mk.x86_64-linux')
        platform.filter('\tMYINCLUDES\t=.*', '\tMYINCLUDES\t= -I. -I%s \\' % spec['netcdf-fortran'].prefix.include)
        platform.filter('\t\t\t  -lnetcdff.*', '\t\t\t  -L%s -lnetcdff \\' % spec['netcdf-fortran'].prefix.lib)
        platform.filter('\tCC\t\t=.*', '\tCC\t\t= %s' % spack_cc)
        platform.filter('\tFC\t\t=.*', '\tFC\t\t= %s' % spack_fc)
        platform.filter('\tF77\t\t=.*', '\tFC\t\t= %s' % spack_f77)
        platform.filter('\tLD\t\t=.*', '\tLD\t\t= %s' % spack_fc)
        platform.filter('\tLDFLAGS\t\t=.*', '\tLDFLAGS\t\t= -m64 -L/lib64 -L/lib -lgfortran -export-dynamic')

    def setup_run_environment(self, env):
        env.set('FER_DIR', self.prefix)
        env.set('FER_GO', ' '.join(['.', self.prefix.go, self.prefix.examples,
                                    self.prefix.contrib]))
        env.set('FER_EXTERNAL_FUNCTIONS', self.prefix.ext_func.libs)
        env.set('FER_PALETTE', ' '.join(['.', self.prefix.ppl]))
        env.set('FER_FONTS', self.prefix.ppl.fonts)

        fer_data = ['.']
        fer_descr = ['.']
        fer_grids = ['.']

        if '+datasets' in self.spec:
            env.set('FER_DSETS', self.prefix.fer_dsets)

            fer_data.append(self.prefix.fer_dsets.data)
            fer_descr.append(self.prefix.fer_dsets.descr)
            fer_grids.append(self.prefix.fer_dsets.grids)

        fer_data.extend([self.prefix.go, self.prefix.examples])
        env.set('FER_DATA', ' '.join(fer_data))
        env.set('FER_DESCR', ' '.join(fer_descr))
        env.set('FER_GRIDS', ' '.join(fer_grids))
