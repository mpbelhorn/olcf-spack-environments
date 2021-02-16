# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os, sys
from spack import *
from subprocess import Popen, PIPE
from time import sleep
from shutil import copytree


class SpectrumMpi(Package):
    """IBM MPI implementation from Spectrum MPI."""

    homepage = "http://www.ibm.com"
    url      = "http://www.ibm.com/spectrum-10.1.0.2.tar.bz2"

    version('10.4.0.3-20210112', 'b2089eaf96318f7ced1df47aad50e2dd',
        url='file:///ccs/packages/IBM/02-2021/SMPI/ibm_smpi-10.4.0.03-20210112-rh8.ppc64le.tar.gz')
    version('10.4.0.0-20200604', '420685675b8579d1611614d540e8d3cf',
        url='file:///ccs/packages/IBM/08-2020/SMPI/ibm_smpi-10.4.0.0-20200604-rh8.ppc64le.tar.gz')
    version('10.3.1.2-20200121', '94c6c95693f736373590ec3d3a2398f7',
        url='file:///ccs/packages/IBM/02-2020/SMPI/ibm_smpi-10.3.1.2-20200121-rh7.ppc64le.tar.gz')
    version('10.3.0.1-20190611', '94a7e1efdf9df18ebb6e4b184251de01',
        url='file:///ccs/packages/IBM/06-2019/SMPI/ibm_smpi-10.3.0.1-20190628-rh7.ppc64le_with_license.tar.gz')
    version('10.3.0.0-20190419', '23a91acf1d7d47d447379e29f103b280',
        url='file:///ccs/packages/IBM/04-19-2019/SMPI/ibm_smpi-10.3.0.0-20190419-rh7.ppc64le.tar.gz')
    version('10.2.0.11-20190201', '8ede33376477f36bb0c150ea0b1cbcc9',
        url='file:///ccs/packages/IBM/01-2019/SMPI/ibm_smpi-10.2.0.11-20190201-rh7.ppc64le.tar.gz')
    version('10.2.0.10-20181214', '4eda8944ad9710f61c79dffaeb0a7bef',
        url='file:///ccs/packages/IBM/12-14-2018/SMPI/ibm_smpi-10.2.0.10-20181214-rh7.ppc64le.tar.gz')
    version('10.2.0.7-20180830', '17eb24e17a4b77c83883aa2a0ff12d49',
        url='file:///ccs/packages/IBM/08-2018/SMPI-20180830/ibm_smpi-10.2.0.7-20180830-rh7.ppc64le.tar.gz')
    version('10.2.0.6-20180813', '5c27b9ebb6eccf08571fb39ef7f67639',
        url='file:///ccs/packages/IBM/08-2018/SMPI-20180813/ibm_smpi-10.2.0.6-20180813-rh7.ppc64le.tar.gz')
    version('10.2.0.5-20180802', 'eeec091457057d08e9d52d475362a32a',
        url='file:///ccs/packages/IBM/08-2018/SMPI/ibm_smpi-10.2.0.5-20180802-rh7.ppc64le.tar.gz')
    version('10.2.0.4-20180716', '5278a7fb2b9bdfb3c60f4e9938449157',
        url='file:///ccs/packages/IBM/07-2018/SMPI/ibm_smpi-10.2.0.4-20180716-rh7.ppc64le.tar.gz')
    version('10.2.0.3-20180611', '24e5454b22ec52192b16a791ea53714c',
        url='file:///ccs/packages/IBM/06-2018/SMPI/ibm_smpi-10.2.0.3-20180611-rh7.ppc64le.tar.gz')
    version('10.2.0.2-20180601', '6e5fab6dfb1f45922ea41e2b420cb6fc',
        url='file:///ccs/packages/IBM/06-2018/SMPI/ibm_smpi-10.2.0.2-20180601-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20180518', 'a9719321d8bf318999aaf9a8421d8d3e',
        url='file:///ccs/packages/IBM/05-2018/SMPI/ibm_smpi-10.2.0.0-20180518-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20180508', '27a9900393d8aa95781d3552dd6e1887',
        url='file:///ccs/packages/IBM/05-2018/SMPI/ibm_smpi-10.2.0.0-20180508-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20180430', '49b051b407c74ca24b07b78c97b491f3',
        url='file:///ccs/packages/IBM/04-2018/smpi/20180430/ibm_smpi-10.2.0.0-20180430-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20180406', 'ecb84bff72b25e7f4bcb1ff8b6080435',
        url='file:///ccs/packages/IBM/04-2018/smpi/ibm_smpi-10.2.0.0-20180406-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20180110', '4221f186c23e18cfac78103e51c73b0c',
        url='file:///ccs/packages/IBM/02-2018/SMPI/ibm_smpi-10.2.0.0-20180110-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20171117', '56a848fc1a1ff8e15d2f2311c38acd87',
        url='file:///ccs/packages/IBM/PRPQ-4Q17-Update/smpi/ibm_smpi-10.2.0.0-20171117-rh7.ppc64le.tar.gz')
    version('10.2.0.0-20171107', '3275c803a6c85c1155afc3cf36d615a0',
        url='file:///ccs/packages/IBM/PRPQ-4Q17/Spectrum_MPI/ibm_smpi-10.2.0.0-20171107-rh7.ppc64le.tar.gz')
    version('10.1.1.0-20170928', 'c77b73979fc38f407effbf20b1862779',
        url='file:///ccs/packages/IBM/09-2017/ibm_smpi-10.1.1.0-20170928-rh7.ppc64le.tar.gz')
    version('10.1.0.4-20170915', '87309d54cdf5ee1cf5745940a3ed0768',
        url='file:///ccs/packages/IBM/09-2017/ibm_smpi-10.1.0.4-20170915-rh7.3.ppc64le.tar.gz')
    version('10.1.0.3-20170713', '382d43fea2ca6628789f65a318b67442',
        url='file:///ccs/packages/IBM/07-2017/ibm_smpi-10.1.0.3jsm_20170713-rh7_Jul13.ppc64le.tar.gz')
    version('10.1.0.3-20170501', '23c7fdda4a214bf0e61f6eff38e0b4ee',
        url='file:///ccs/packages/IBM/05-2017/ibm_smpi-10.1.0.3.20170501-rh7.3.ppc64le.tar.gz')
    version('10.1.0.2', '59d391ebe0818defe30c55443cc7ea92',
        url='file:///ccs/packages/IBM/05-2017/ibm_smpi-10.1.0.2-rh7.3.ppc64le.tar.gz')

    provides('mpi')

    def install(self, spec, prefix):
        rpms = [i for i in os.listdir('.') if i.endswith('ppc64le.rpm')]
        rpm2cpio = which('rpm2cpio')
        for _rpm in rpms:
            rpm2cpio = Popen(['rpm2cpio', _rpm],
                             stdout=PIPE)
            cpio = Popen('cpio -idmv'.split(),
                         stdin=rpm2cpio.stdout,
                         stdout=PIPE)
            cpio.communicate()
        chmod = which('chmod')
        unpacked = join_path(self.stage.source_path, 'opt/ibm/spectrum_mpi')
        chmod('-R', 'ug+rwX', unpacked)
        if os.path.exists('patch.tgz'):
            tar = which('tar')
            tar('xzvf', 'patch.tgz')
        for f in os.listdir(unpacked):
            src = join_path(unpacked, f)
            dst = join_path(self.prefix, f)
            copytree(src, dst, symlinks=True)
            # # This is the normal way to install RPMs but is broken by IBM's
            # # root-only, non-relocatable structure used in earlier Spectrum
            # # releases.
            # rpm_bin = which('rpm')
            # rpm_bin('-iv',
            #         '--nodeps',
            #         '--dbpath=%s' % join_path(self.stage.path, 'rpmdb'),
            #         '--prefix=%s' % self.prefix,
            #         '--replacepkgs',
            #         '*.ppc64le.rpm')

    def accept_license(self):
        # Post install
        # Accept license
        accept_license = Executable(join_path(self.prefix, 'lap_se/lapc'))
        lap_se = '%s/lap_se/' % self.prefix
        accept_license('-l', lap_se, '-s', lap_se, '-t', '5', ignore_errors=(9,))

    def _fix_syntax_error(self):
        '''Patch mpi.h post-install to correct issues where the compiler cannot
        be identified by build systems because of a syntax error in a macro that
        injects SMPI_BUILT_AGAINST_VERSION string into user's code if
        SMPI_HAVE_PRAGMA_WEAK=1. The bad code is nominally around line 278 in
        mpi.h for versions of SMPI since 10.4.
        '''
        # TODO: Check that this patch is still relevent for each future release
        # of SMPI and limit the versions when it has been fixed.
        if self.spec.satisfies('@10.4:'):
            filter_file(r'(#if\s*\(\s*)1(\s*==\s*SMPI_HAVE_PRAGMA_WEAK.*)',
                        r'\12\2',
                        '%s/mpi.h' % self.prefix.include)

    def _rebuild_fortran_mod_script(self):
        '''Run ./build.sh fortran module rebuild script in an appropriate
        environment.
        '''
        module_build = Executable('./build.sh')
        mod_env = os.environ
        compiler_env_options = {
                'MPI_ROOT': self.prefix.replace('/autofs/nccs-svm1_', '/'),
                'OMPI_FC': self.compiler.fc,
                'OMPI_CC': self.compiler.cc,
                }
        if '%xl' in self.spec:
            compiler_env_options.update({
                'FORTSUPPORT_PIC_FFLAGS': '-qPIC',
                'FORTSUPPORT_PIC_CFLAGS': '-qPIC',
                'FORTSUPPORT_PIC_LDFLAGS': '-qPIC -qmkshrobj',
                })
        mod_env.update(compiler_env_options)
        module_build(env=mod_env)

    def _rebuild_fortran_mod_20200604(self):
        '''Rebuild fortran modules for the specific compiler in use for versions
        up to and including 10.4.0.0-20200604.
        '''
        # Rebuild fortran modules for the specific compiler in use.
        spec = self.spec
        mod_src_dir = join_path(self.prefix, 'lib', 'module')
        _compiler_is_pgi = spec.satisfies('%pgi') or spec.satisfies('%nvhpc')
        if spec.satisfies('@10.4.0.0-20200604') and _compiler_is_pgi:
            mod_src_dir = join_path(self.prefix, 'lib', 'pgi')
        with working_dir(mod_src_dir):
            self._rebuild_fortran_mod_script()
            cp = which('cp')
            cp('-u', 'mpi.mod', '../.')
            if _compiler_is_pgi and os.path.exists('./include/mpif-sizeof.h'):
                cp('-u', './include/mpif-sizeof.h', '../../include/.')

    def _rebuild_fortran_mod_20210112(self):
        '''Rebuild fortran modules for the specific compiler in use for versions
        10.4.0.3-20210112 and potentially forward.
        '''
        return
        # FIXME: 10.4.0.3-20210112 is missing headers needed to rebuild the
        # fortran modules for the current (any) compiler. Otherwise, we would do
        # the following:
        mod_src_dir = join_path(self.prefix, 'lib', 'fortsupport_rebuild')
        with working_dir(mod_src_dir):
            self._rebuild_fortran_mod_script()
            # FIXME: copy out modules and headers to appropriate locations.
            cp = which('cp')
            cp('-u', '*.mod', '../.')
            cp('-u', '*.h', '../../include/.')

    def _smpi_conf_20200121(self):
        '''Correct the symlink to smpi.conf for current MOFED version.
        
        This function always updates the conf to v4.7.3 but should probably
        parse `ofed_info` and adjust it as necessary.
        '''
        etc_dir = self.spec.prefix.etc
        (link_name, tmp_link_name, link_target) = [
            join_path(etc_dir, name) for name in ('smpi.conf',
                                                  'tmp_smpi.conf',
                                                  'smpi-MOFED-4_7_3.conf')
            ]
        if not os.path.exists(link_target):
            return

        # Create symlink to target and then move it over existing symlink to
        # update link atomically.
        os.symlink(link_target, tmp_link_name)
        os.rename(tmp_link_name, link_name)

    @run_after('install')
    def post_install(self):
        '''Run post-install corrections to SMPI.
        
        IBM changes paths and procedures virtually every release so we have
        split the post-install tasks into private methods and apply them to the
        appropriate versions in sequence here.
        '''
        spec = self.spec
        self.accept_license()
        self._fix_syntax_error()

        if spec.satisfies('@10.3.1.2-20200121'):
            # Only v10.3.1.2
            self._smpi_conf_20200121()
            self._rebuild_fortran_mod_20200604()
        if spec.satisfies('@:10.4.0.0-20200604'):
            # all versions up to 10.4.0.0
            self._rebuild_fortran_mod_20200604()
        elif spec.satisfies('@10.4.0.3-20210112'):
            # Version 10.4.0.3 and possible future.
            self._rebuild_fortran_mod_20210112

    def setup_dependent_package(self, module, dspec):
        # get library name and directory
        self.spec.mpi_base_dir = self.prefix
        self.spec.mpi_library = join_path(self.prefix.lib, 'libmpi_ibm.so')
        self.spec.mpi_include_path = self.prefix.include
        self.spec.mpi_library_path = self.prefix.lib
        self.spec.mpi_np_flag = '--np'
        if '%xl' in dspec or '%xl_r' in dspec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpixlc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpixlC')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpixlf')
        else:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpifort')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpifort')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpifort')


    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpixlc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpixlC'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpixlf'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpixlf'))
        else:
            spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpifort'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpifort'))

        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)

        spack_env.set('OMPI_DIR', self.prefix)
        spack_env.set('MPI_DIR', self.prefix)
        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)


    def setup_environment(self, spack_env, run_env):

        run_env.set('OMPI_DIR', self.prefix)
        run_env.set('MPI_ROOT', self.prefix)
        run_env.set('OPAL_PREFIX', self.prefix)
        run_env.set('OPAL_LIBDIR', self.prefix.lib)

        run_env.set('OMPI_CC', self.compiler.cc)
        run_env.set('OMPI_CXX', self.compiler.cxx)
        run_env.set('OMPI_FC', self.compiler.fc)

