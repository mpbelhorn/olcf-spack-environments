# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class DarshanRuntime(Package):
    """Darshan (runtime) is a scalable HPC I/O characterization tool
    designed to capture an accurate picture of application I/O behavior,
    including properties such as patterns of access within files, with
    minimum overhead. DarshanRuntime package should be installed on
    systems where you intend to instrument MPI applications."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"
    git      = "https://xgitlab.cels.anl.gov/darshan/darshan.git"

    maintainers = ['shanedsnyder', 'carns', 'mpbelhorn']

    version('develop', branch='master')
    version('3.2.1', sha256='d63048b7a3d1c4de939875943e3e7a2468a9034fcb68585edbc87f57f622e7f7')
    version('3.2.0', sha256='4035435bdc0fa2a678247fbf8d5a31dfeb3a133baf06577786b1fe8d00a31b7e')
    version('3.1.8', sha256='3ed51c8d5d93b4a8cbb7d53d13052140a9dffe0bc1a3e1ebfc44a36a184b5c82')
    version('3.1.7', sha256='9ba535df292727ac1e8025bdf2dc42942715205cad8319d925723fd88709e8d6')
    version('3.1.6', sha256='21cb24e2a971c45e04476e00441b7fbea63d2afa727a5cf8b7a4a9d9004dd856')
    version('3.1.0', sha256='b847047c76759054577823fbe21075cfabb478cdafad341d480274fb1cef861c')
    version('3.0.0', sha256='95232710f5631bbf665964c0650df729c48104494e887442596128d189da43e0')

    depends_on('mpi', when='+mpi')
    depends_on('zlib')

    variant('slurm', default=False, description='Use Slurm Job ID')
    variant('cobalt', default=False, description='Use Cobalt Job Id')
    variant('pbs', default=False, description='Use PBS Job Id')
    variant('lsf', default=False, description='Use LSF Job Id')
    variant('mpi', default=True, description='Compile with MPI support')
    variant('grouplogs', default=False,
            description='Make logs files group-readable')
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
    patch('darshan-pkgconfig-cray.patch', when='platform=cray')

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
        options = []
        if '+mpi' in spec:
            options = ['CC=%s' % spec['mpi'].mpicc]
        else:
            options = ['--without-mpi']
        options.extend(['--with-mem-align=8',
                        '--with-jobid-env=%s' % job_id,
                        '--with-zlib=%s' % spec['zlib'].prefix])

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

    def setup_run_environment(self, env):
        if self.spec.satisfies('^spectrum-mpi'):
            env.set('OMPI_LD_PRELOAD_PREPEND',
                    join_path(prefix, 'lib', 'libdarshan.so'))

        if self.spec.satisfies('platform=cray'):
            env.prepend_path('PE_PKGCONFIG_LIBS', 'darshan-runtime')
