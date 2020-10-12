whatis([[Name : pgi]])
whatis([[Version : 20.1]])
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

local prefix = "/sw/summit/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg"

prepend_path("CMAKE_PREFIX_PATH", prefix, ":")
setenv("CC", pathJoin(prefix, "linuxpower/20.1/bin/pgcc"))
setenv("CXX", pathJoin(prefix, "linuxpower/20.1/bin/pgc++"))
setenv("F77", pathJoin(prefix, "linuxpower/20.1/bin/pgfortran"))
setenv("FC", pathJoin(prefix, "linuxpower/20.1/bin/pgfortran"))
prepend_path("PATH", pathJoin(prefix, "linuxpower/20.1/bin"), ":")
prepend_path("LD_LIBRARY_PATH", pathJoin(prefix, "linuxpower/20.1/lib"), ":")
prepend_path("MANPATH", pathJoin(prefix, "linuxpower/20.1/man"), ":")
setenv("OLCF_PGI_ROOT", prefix)
