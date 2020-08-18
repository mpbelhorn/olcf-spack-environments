# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.prefix import Prefix
import os


class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: The PGI compilers are licensed software. You will need to create an
    account on the PGI homepage and download PGI yourself. Spack will search
    your current directory for the download tarball. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.pgroup.com/"

    version('20.1',  '9653c1e5dd8622f21cc7d45e10dbbd27', url='file:///ccs/packages/IBM/02-2020/PGI/pgilinux-2020-201-ppc64le.tar.gz')
    version('19.10',  '9afe557f3e80b8b0fe9a2894b9906989', url='file:///ccs/packages/IBM/10-2019/PGI/pgilinux-2019-1910-ppc64le.tar.gz')
    version('19.9',  'a4f2b956f20a66745b5b51780a3573a8', url='file:///ccs/packages/IBM/09-2019/PGI/pgilinux-2019-199-ppc64le.tar.gz')
    version('19.7',  '7c3928b45a282d55ebb3c31a2dff214e', url='file:///ccs/packages/IBM/08-2019/PGI/pgilinux-2019-197-ppc64le.tar.gz')
    version('19.5',  'd75ea928c5f0385fd4ee4ba30d483ef1', url='file:///ccs/packages/IBM/05-2019/PGI/pgilinux-2019-195-ppc64le.tar.gz')
    version('19.4',  '50383cbf56ae154d6b3bdb7904ed0303', url='file:///ccs/packages/IBM/05-2019/PGI/pgilinux-2019-194-ppc64le.tar.gz')
    version('19.3',  '33fb9ac82e680b92c4a412c4f49fde3d', url='file:///ccs/packages/IBM/04-19-2019/PGI/pgilinux-2019-193-ppc64le.tar.gz')
    version('19.1',  'de6cc7611c7fd3e6cc5d2a568c9e1c85', url='file:///ccs/packages/IBM/02-2019/PGI/pgilinux-2019-191-ppc64le.tar.gz')
    version('18.10',  'fbaa8e380a6fa53700aec217b0bc4271', url='file:///ccs/packages/IBM/12-14-2018/PGI/pgilinux-2018-1810-ppc64le.tar.gz')
    version('18.7',  '6cbec1d342bc522caa367875e410e033', url='file:///ccs/packages/IBM/08-2018/PGI/pgilinux-2018-187-ppc64le.tar.gz')
    version('18.5',  '70393f462e143bbefd6940530c8d2475', url='file:///ccs/packages/IBM/07-2018/PGI/pgilinux-2018-185-ppc64le.tar.gz')
    version('18.4',  '591c1d7ed80e9a392dcd19392c72b9dc', url='file:///ccs/packages/IBM/04-2018/PGI/pgilinux-2018-184-ppc64le.tar.gz')
    version('18.3',  'a6bd64352af793526d1b0fd9206823e3', url='file:///ccs/packages/IBM/03-2018/PGI/pgilinux-2018-183-ppc64le.tar.gz')
    version('18.1',  '5281f5772f8abe1374012208eeadef62', url='file:///ccs/packages/IBM/02-2018/PGI/pgilinux-2018-181-ppc64le.tar.gz')
    version('17.10', 'bedb8a4fdfdbb7d023ac76437d41e8f9', url='file:///ccs/packages/IBM/11-2017/PGI/pgilinux-2017-1710-ppc64le.tar.gz')
    version('17.9',  '9e0f2d22ddfb39d615b72e79e57bb76f', url='file:///ccs/packages/IBM/10-2017/PGI/pgilinux-2017-179-ppc64le.tar.gz')
    version('17.7',  'b6bdfb968e24a9c69387bf002847df84', url='file:///ccs/packages/IBM/08-2017/PGI/pgilinux-2017-177-ppc64le.tar.gz')
    version('17.5',  '32e1d566abc6a846ca39ca99777d21d4', url='file:///ccs/packages/IBM/05-2017/PGI/pgilinux-2017-175-ppc64le.tar.gz')

    variant('network', default=True,
            description="Perform a network install")
    variant('single',  default=False,
            description="Perform a single system install")
    variant('nvidia',  default=False,
            description="Enable installation of optional NVIDIA components")
    variant('amd',     default=False,
            description="Enable installation of optional AMD components")
    variant('java',    default=False,
            description="Enable installation of Java Runtime Environment")
    variant('mpi',     default=False,
            description="Enable installation of Open MPI")
    variant('managed',     default=False,
            description="Enable managed memory")
    variant('mpigpu',     default=False,
            description="Enable GPU aware MPI")

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['license.pgi']
    license_vars = ['PGROUPD_LICENSE_FILE', 'LM_LICENSE_FILE']
    license_url = 'http://www.pgroup.com/doc/pgiinstall.pdf'

    _true_prefix = None

    @property
    def true_prefix(self):
        prefix = getattr(self, '_true_prefix', None)
        if not prefix:
            target = str(self.spec.architecture.target).lower()
            if any((i in target for i in ('power', 'ppc'))):
                if 'linux' in self.spec.architecture.platform:
                    prefix = join_path(self.prefix,
                                       'linuxpower',
                                       str(self.spec.version).split('-')[0])
            elif 'x86_64' in target:
                    prefix = join_path(self.prefix,
                                       'linux86-64',
                                       str(self.spec.version).split('-')[0])
        if not prefix:
            raise Exception("Cannot determine true PGI prefix!")
        self._true_prefix = prefix
        return self._true_prefix

    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['PGI_SILENT'] = "true"
        os.environ['PGI_ACCEPT_EULA'] = "accept"
        os.environ['PGI_INSTALL_DIR'] = prefix

        if '+network' in spec and '~single' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "network"
            os.environ['PGI_INSTALL_LOCAL_DIR'] = "%s/%s/share_objects" % \
                (prefix, self.version)
        elif '+single' in spec and '~network' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "single"
        else:
            msg  = 'You must choose either a network install or a single '
            msg += 'system install.\nYou cannot choose both.'
            raise RuntimeError(msg)

        if '+nvidia' in spec:
            os.environ['PGI_INSTALL_NVIDIA'] = "true"

        if '+amd' in spec:
            os.environ['PGI_INSTALL_AMD'] = "true"

        if '+java' in spec:
            os.environ['PGI_INSTALL_JAVA'] = "true"

        if '+mpi' in spec:
            os.environ['PGI_INSTALL_MPI'] = "true"

        if '+mpigpu' in spec:
            os.environ['PGI_MPI_GPU_SUPPORT'] = "true"

        if '+managed' in spec:
            os.environ['PGI_INSTALL_MANAGED'] = "true"

        # Run install script
        os.system("./install")

       
        # FIXME - This is arch-specific.
        siterc_file = join_path(self.true_prefix, 'bin', 'siterc')
        with open(siterc_file, 'a') as siterc:
            siterc.write("append SITEDEF=__ORDER_BIG_ENDIAN__=4321;\n")
            siterc.write("append SITEDEF=__ORDER_LITTLE_ENDIAN__=1234;\n")
            siterc.write("append SITEDEF=__ORDER_PDP_ENDIAN__=3412;\n")
            siterc.write("append SITEDEF=__BYTE_ORDER__=__ORDER_LITTLE_ENDIAN__;\n")

    def setup_environment(self, spack_env, run_env):
        # FIXME - generalize arch
        prefix = Prefix(self.true_prefix)

        run_env.set('CC',  join_path(prefix.bin, 'pgcc'))
        run_env.set('CXX', join_path(prefix.bin, 'pgc++'))
        run_env.set('F77', join_path(prefix.bin, 'pgfortran'))
        run_env.set('FC',  join_path(prefix.bin, 'pgfortran'))

        run_env.prepend_path('PATH',            prefix.bin)
        run_env.prepend_path('CPATH',           prefix.include)
        run_env.prepend_path('LIBRARY_PATH',    prefix.lib)
        run_env.prepend_path('LD_LIBRARY_PATH', prefix.lib)
        run_env.prepend_path('MANPATH',         prefix.man)
