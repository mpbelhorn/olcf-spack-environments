-- -*- lua -*-
-- Module file created by spack (https://github.com/spack/spack) on 2020-09-16 14:14:26.821949
--
-- pgi@20.4%gcc@8-os~amd~java+managed+mpi+mpigpu~network+nvidia+single arch=linux-rhel8-ppc64le/oy4x2h7
--

whatis([[Name : pgi]])
whatis([[Version : 20.4]])
whatis([[Target : ppc64le]])
whatis([[Short description : PGI optimizing multi-core compilers for Linux with support for debugging and profiling of local MPI processes.]])

help([[PGI optimizing multi-core compilers for Linux, MacOS & Windows with
support for debugging and profiling of local MPI processes.]])

-- Services provided by the package
family("compiler")

local platform = 'linux-rhel8-ppc64le'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

local prefix = "/FIXME"

prepend_path("CMAKE_PREFIX_PATH", prefix, ":")
setenv("CC", pathJoin(prefix, "linuxpower/20.4/bin/pgcc"))
setenv("CXX", pathJoin(prefix, "linuxpower/20.4/bin/pgc++"))
setenv("F77", pathJoin(prefix, "linuxpower/20.4/bin/pgfortran"))
setenv("FC", pathJoin(prefix, "linuxpower/20.4/bin/pgfortran"))
prepend_path("PATH", pathJoin(prefix, "linuxpower/20.4/bin"), ":")
prepend_path("LD_LIBRARY_PATH", pathJoin(prefix, "linuxpower/20.4/lib"), ":")
prepend_path("MANPATH", pathJoin(prefix, "linuxpower/20.4/man"), ":")
setenv("OLCF_PGI_ROOT", prefix)
