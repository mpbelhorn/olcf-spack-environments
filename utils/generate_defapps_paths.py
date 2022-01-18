#!/usr/bin/env python3
'''
generate_defapps_paths: A utility for identifying and sorting the modulepaths
elements for spack-generated modules that depend on cray-mpich. The output of
this script is used to update the modulepaths controlled by DefApps when various
PrgEnv-*, compiler, and possibly even cray-mpich modules are loaded by users.

Available cray-mpich-dependent module tree paths are sorted by
    - compiler
    - compiler version
    - cray-mpich version
    - installation date

Without arguments, this script attempts to identify the system the script is
called from and show cray-mpich modulepath elements for that system. Optionally,
a single <host> argument can be given where spack-installed environment modules
are looked for under the path:

    ```
    /sw/<host>/spack-envs/base/modules/spack
    ```

'''

import os
from os.path import join as joinpath, dirname, basename, isdir
from distutils.version import LooseVersion


def walk_depth(root, max_depth=2):
    '''A modified version of `os.walk`.

    `walk_depth` stops descending into subdirectories past `max_depth`.
    '''
    nroot = os.path.normpath(root)
    depth_offset = nroot.count(os.sep) - 1

    for path, dirs, files in os.walk(nroot, topdown=True):
        yield path, dirs, files
        # If depth is at maximum, clear dirs to stop descending further
        if (path.count(os.sep) - depth_offset) >= max_depth:
            dirs[:] = []


class MpiModuleRoot:
    '''Abstract representation of the LMOD hierarchy directory into which spack
    installs modules for packages that depend on cray-mpich.
    '''
    def __init__(self, path):
        compiler_path = dirname(path)
        mpich_path = dirname(compiler_path)

        self.path = path
        self.compiler_version = LooseVersion(basename(path))
        self.compiler_name = basename(compiler_path)
        _mpi_version, self.mpi_id = basename(mpich_path).split('-')
        self.mpi_version = LooseVersion(_mpi_version)
        self.timestamp = os.path.getctime(path)

    def __repr__(self):
        return 'cray-mpich({mpi_version}, {compiler_name}/{compiler_version})'.format(
            compiler_name=self.compiler_name,
            compiler_version=self.compiler_version,
            mpi_version=self.mpi_version)

    def validate(self):
        '''Check if modulefile root path actually exists.'''
        return isdir(self.path)


class MpiModules:
    '''Sorted collection of all cray-mpich-dependent LMOD hierarchy roots'''
    def __init__(self, host):
        '''Find and sort all cray-mpich-dependent LMOD hierarchy roots.

        Looks for module roots associated with the canonical system name `host`,
        eg: "frontier", "crusher", etc.
        '''
        self.host = host
        self.module_prefix = joinpath('/sw',
                                      host,
                                      'spack-envs/base/modules/spack')
        self.unique_mpis = list()

        for path in self.mpich_module_root_dirs():
            selection_depth = path.count(os.sep) + 2
            for root, dirs, _ in walk_depth(path, 3):
                if root.count(os.sep) != selection_depth or not dirs:
                    continue
                tree_path = joinpath(root, dirs[0])
                if not isdir(tree_path):
                    continue
                self.unique_mpis.append(MpiModuleRoot(tree_path))
        self.unique_mpis.sort(
            reverse=True,
            key=lambda x: [x.compiler_name,
                           x.compiler_version,
                           x.mpi_version,
                           x.timestamp])

    def mpich_module_root_dirs(self):
        '''Yield LMOD hierarchy paths ending with a `cray-mpich` directory.'''
        for root, dirs, _ in walk_depth(self.module_prefix, 2):
            if 'cray-mpich' in dirs:
                yield joinpath(root, 'cray-mpich')

    def show_paths(self):
        '''Displays the found cray-mpich module roots in sorted order.'''
        compiler_name = ''
        compiler_version = ''
        for mpi in self.unique_mpis:
            if compiler_name != mpi.compiler_name:
                compiler_name = mpi.compiler_name
                print('{0}:'.format(compiler_name))
            if compiler_version != str(mpi.compiler_version):
                compiler_version = mpi.compiler_version
                print('  {0}:'.format(compiler_version))
            print('    {0}'.format(mpi.path))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        sysname = sys.argv[1]
    else:
        # Default to 'spock' if sysname is not given or cannot be found
        sysname = os.getenv('LMOD_SYSTEM_NAME', 'spock')
    trees = MpiModules(sysname)
    trees.show_paths()
