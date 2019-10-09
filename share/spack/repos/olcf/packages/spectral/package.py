##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import os
from spack import *


class Spectral(CMakePackage):
    """Spectral is a portable and transparent middleware library to enable use
    of the node-local burst buffers for accelerated application output on
    Summit/Sierra-like IBM machines. Spectral does this by using library
    intercept techniques to take advantage of IBM BBAPI calls when available.
    """

    homepage = "https://code.ornl.gov/cz7/Spectral"
    git = "https://code.ornl.gov/cz7/Spectral.git"

    version('20190401', commit='67dc9e891d83d11afefb0e1da690fdd92ee2ff3c')
    version('20181227', commit='d2ac1dbb50f32e2b62db93ef175d25d624299be3')

    variant('debug', default=False, description='Enable debugging symbols')
    variant('titan', default=False, description='Enable Titan emulation')
    variant('examples', default=False, description='Build examples')

    depends_on('mpi', when="+examples")

    @property
    def prologue_entrypoint(self):
        '''Return format string using OLCF SWCI variables to path used by batch
        scheduler prologue scripts or empty string if prologue entrypoint should
        not be updated. This string is used by the olcf_prologue_link
        post_install hook.
        '''
        tier = os.environ.get('SWCI_TIER', '')
        if tier.startswith('0') and self.spec.satisfies('~titan~examples'):
            return '{host_dir}/spectral/usr/local'
        return ''

    def patch(self):
        """Disable building the examples."""
        if not self.spec.satisfies('+examples'):
            filter_file(r'(^\s*)(add_subdirectory\(examples\))',
                        r'\1#\2',
                        "CMakeLists.txt")

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+debug'):
            args.append('-DDEBUG')

        if self.spec.satisfies('+titan'):
            args.append('-DTITAN')

        return args

    def setup_environment(self, spack_env, run_env):
        run_env.set('OMPI_LD_PRELOAD_PREPEND',
                    join_path(self.prefix, 'lib', 'libspectral.so'))

        # TODO: Set announcement in
        # /sw/${HOST}/lmod/${VER}/${BUILD}/lmod/etc/admin.list
        # regarding the following variables which are set in lua modulefile
        # template only.
        # run_env.set('PERSIST_DIR', "'/mnt/bb' .. os.getenv('USER')")
        # run_env.set('PSF_DIR', "os.getenv('MEMBEWORK') or ''")
