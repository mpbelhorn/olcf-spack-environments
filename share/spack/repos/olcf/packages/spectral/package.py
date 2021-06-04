# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from llnl.util.filesystem import mkdirp
import llnl.util.tty as tty
from spack import *


class Spectral(CMakePackage):
    """Spectral is a portable and transparent middleware library to enable use
    of the node-local burst buffers for accelerated application output on
    Summit/Sierra-like IBM machines. Spectral does this by using library
    intercept techniques to take advantage of IBM BBAPI calls when available.
    """

    homepage = "https://code.ornl.gov/cz7/Spectral"
    git = "https://code.ornl.gov/cz7/Spectral.git"

    version('20210521', commit='c3bb9b7ed849da85a6fe488ec82f0041736904f9')
    version('20210514', commit='1f9668dda0dc06643da52d8d0bc0242460f8d7cb')
    version('20190401', commit='67dc9e891d83d11afefb0e1da690fdd92ee2ff3c')
    version('20181227', commit='d2ac1dbb50f32e2b62db93ef175d25d624299be3')

    variant('debug', default=False, description='Enable debugging symbols')
    variant('titan', default=False, description='Enable Titan emulation')
    variant('examples', default=False, description='Build examples')
    variant('prologue_dir', default='none',
            description='Path to LFS prologue script dir',
            multi=False)

    depends_on('mpi', when="+examples")
    depends_on('log4c', when='@20210514:')
    depends_on('glib@:2.99', when='@20210514:')
    depends_on('pkgconf', type='build')

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
        # At runtime, users must also set the following envvars
        #     (arbitrary values for <fields in rangle/langle brackets>)
        # 'PERSIST_DIR="/mnt/bb/$USER"'
        # 'PSF_DIR="<path on GPFS>"'
        run_env.set('OMPI_LD_PRELOAD_PREPEND',
                    join_path(self.prefix, 'lib', 'libspectral.so'))

    @run_after('install')
    def update_prologue_symlink(self):
        # Summit: prologue_dir="/sw/summit/spectral/usr/local"
        link_name = self.spec.variants['prologue_dir'].value
        if link_name == 'none':
            tty.warn("Skipping prologue symlink update.")
            return
        link_dir = os.path.dirname(link_name)
        target = self.prefix

        if not os.path.exists(target):
            tty.warn("Install prefix '%s' does not exist!" % target)
            return

        try:
            # FIXME: commented code below should be uncommented when ready to
            # deploy symlinks after OS upgrade.
            if not os.path.exists(link_dir):
                tty.msg("'%s' does not exist. Creating directory." % link_dir)
                # mkdirp(link_dir)

            if os.path.exists(link_name):
                old_target = os.readlink(link_name)
                if old_target == target:
                    tty.msg("No update needed for prologue script symlink.")
                    return
                tty.msg("Removing existing symlink '%s --> %s'" %
                        (link_name, old_target))
                # os.remove(link_name)
            tty.msg("Updating symlink for prologue scripts '%s --> %s'" %
                    (link_name, target))
            # os.symlink(target, link_name)
        except OSError as _err:
            tty.warn("Cannot update symlink %s for prologue scripts to %s" %
                     (link_name, target))
