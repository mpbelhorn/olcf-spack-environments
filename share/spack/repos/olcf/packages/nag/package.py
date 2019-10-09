# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Nag(Package):
    """The NAG Fortran Compiler."""
    homepage = "http://www.nag.com/nagware/np.asp"

    version('6.1', '0040d2254258223c78a6a4ab4829d7e0')
    version('6.0', '3fa1e7f7b51ef8a23e6c687cdcad9f96')
    version('fl24', '25a3c4d5924d02166f7a99dc159e187b')

    # Licensing
    license_required = True
    license_comment = '!'
    license_files = ['lib/nag.key']
    license_vars = ['NAG_KUSARI_FILE']
    license_url = 'http://www.nag.com/doc/inun/np61/lin-mac/klicence.txt'

    def url_for_version(self, version):
        # TODO: url and checksum are architecture dependent
        # TODO: We currently only support x86_64
        url = 'http://www.nag.com/downloads/impl/npl6a{0}na_amd64.tgz'
        return url.format(version.joined)

    def install(self, spec, prefix):
        # Set installation directories
        os.environ['INSTALL_TO_BINDIR'] = prefix.bin
        os.environ['INSTALL_TO_LIBDIR'] = prefix.lib
        os.environ['INSTALL_TO_MANDIR'] = prefix + '/share/man/man'

        # Run install script
        os.system('./INSTALLU.sh')

    def setup_environment(self, spack_env, run_env):
        run_env.set('F77', join_path(self.prefix.bin, 'nagfor'))
        run_env.set('FC',  join_path(self.prefix.bin, 'nagfor'))

    # The fl24 version required by NCRC is cut from an entirely different cloth
    # and might as well be considered a totally separate program given how
    # different it's installation and runtime environment is. The exceptions are
    # handled below.
    @when('@fl24')
    def url_for_version(self, version):
        return 'http://nag.com/downloads/impl/fll6a24dpl.tgz'

    @when('@fl24')
    def install(self, spec, prefix):
        os.system('./install.sh -accept -installdir=%s' % prefix)

    @when('@fl24')
    def setup_environment(self, spack_env, run_env):
        nagdir = "%s/fll6a24dpl" % self.prefix
        run_env.set('NAGDIR', nagdir)
        run_env.set('NAG_POST_LINK_OPTS', "-L%s/lib" % nagdir)
        run_env.set('NAG_INCLUDE_OPTS', "")
        run_env.prepend_path('LD_LIBRARY_PATH', "%s/lib" % nagdir)
        run_env.prepend_path('PE_PRODUCT_LIST', 'NAG')
