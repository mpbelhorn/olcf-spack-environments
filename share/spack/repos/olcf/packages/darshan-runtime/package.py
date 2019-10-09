##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class DarshanRuntime(Package):
    """Darshan (runtime) is a scalable HPC I/O characterization tool
    designed to capture an accurate picture of application I/O behavior,
    including properties such as patterns of access within files, with
    minimum overhead. DarshanRuntime package should be installed on
    systems where you intend to instrument MPI applications."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"

    version('3.1.7', '2777e0769ec2b31dd1065f1de835dcfc')
    version('3.1.6', 'ce5b8f1e69d602edd4753b57258b57c1')
    version('3.1.5-pre1', 'a15b47dde695ba5f1eb6129e41c5a8b1')
    version('3.1.4patched', '997e85fdb45ee6e38248e27438210b7c', 
            url='file:///ccs/packages/darshan/darshan-snyder-20171009.tar.gz')
    version('3.1.4', '1d75060d229a36cd65f7ab24b51ddbf5')
    version('3.1.0', '439d717323e6265b2612ed127886ae52')
    version('3.0.0', '732577fe94238936268d74d7d74ebd08')

    depends_on('mpi')
    depends_on('zlib')

    variant('grouplogs', default=False,
            description='Make logs files group-readable')
    variant('slurm', default=False, description='Use Slurm Job ID')
    variant('cobalt', default=False, description='Use Coblat Job Id')
    variant('pbs', default=False, description='Use PBS Job Id')
    variant('lsf', default=False, description='Use LSF Job Id')
    variant('pcpatch', default=False,
            description='Apply pkgconfig patch for Cray systems')
    variant(
        'hdf5', default='none',
        description='Multithreading support',
        values=('pre1.10', 'post1.10', 'none'),
        multi=False
    )
    variant(
        'logpath',
        default='default',
        description='Log Output Path',
        values=lambda x: True,
        multi=False
    )
    patch('darshan-prepend.patch')
    patch('darshan-pkgconfig-cray.patch', when="+pcpatch")

    def install(self, spec, prefix):

        job_id = 'NONE'
        if '+slurm' in spec:
            job_id = 'SLURM_JOBID'
        if '+cobalt' in spec:
            job_id = 'COBALT_JOBID'
        if '+pbs' in spec:
            job_id = 'PBS_JOBID'
        if '+lsf' in spec:
            job_id = 'LSB_JOBID'

        # TODO: BG-Q and other platform configure options
        options = ['CC=%s' % spec['mpi'].mpicc,
                   '--with-mem-align=8',
                   '--with-jobid-env=%s' % job_id,
                   '--with-zlib=%s' % spec['zlib'].prefix]

        if spec.satisfies('+grouplogs'):
            options.append('--enable-group-readable-logs')
        else:
            options.append('--disable-group-readable-logs')

        target_logpath = spec.variants['logpath'].value
        if target_logpath == 'default':
            # Set DARSHAN_LOG_DIR_PATH and DARSHAN_LOGFILE_PREPEND in modules.yaml.
            options.append('--with-log-path-by-env=DARSHAN_LOG_DIR_PATH')
        elif os.path.isabs(target_logpath) and os.path.isdir(target_logpath):
            options.append('--with-log-path=%s' % spec.variants['logpath'].value)
        else:
            raise InstallError("Target log path directory '%s' does not exist."
                    % target_logpath)

        if spec.satisfies('hdf5=pre1.10'):
            options.append('--enable-HDF5-pre-1.10')
        elif spec.satisfies('hdf5=post1.10'):
            options.append('--enable-HDF5-post-1.10')

        with working_dir('spack-build', create=True):
            configure = Executable('../darshan-runtime/configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('install')

    def setup_environment(self, spack_env, run_env):
        if self.spec.satisfies('^spectrum-mpi'):
            run_env.set('OMPI_LD_PRELOAD_PREPEND',
                        join_path(prefix, 'lib', 'libdarshan.so'))

        if self.spec.satisfies('platform=cray'):
            run_env.prepend_path('PE_PKGCONFIG_LIBS', 'darshan-runtime')

