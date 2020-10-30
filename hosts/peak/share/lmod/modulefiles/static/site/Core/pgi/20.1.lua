-- -*- lua -*-
-- Module file created by spack (https://github.com/spack/spack) on 2020-03-18 15:51:08.925099
--
-- pgi@20.1%gcc@4.8.5~amd~java+managed+mpi+mpigpu~network+nvidia+single arch=linux-rhel7-ppc64le /mkkhy2l
--

whatis([[Name : pgi]])
whatis([[Version : 20.1]])
whatis([[Short description : PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows with support for debugging and profiling of local MPI processes.]])

help([[PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows with
support for debugging and profiling of local MPI processes. Note: The
PGI compilers are licensed software. You will need to create an account
on the PGI homepage and download PGI yourself. Spack will search your
current directory for the download tarball. Alternatively, add this file
to a mirror so that Spack can find it. For instructions on how to set up
a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html]])

-- Services provided by the package
family("compiler")

local platform = 'linux-rhel8-ppc64le'
-- local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_module_root = (myFileName():sub(1, myFileName():find(myModuleFullName(),1,true)-2)):gsub("/site/Core.*",'/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

prepend_path("CMAKE_PREFIX_PATH", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg", ":")
setenv("CC", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/bin/pgcc")
setenv("CXX", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/bin/pgc++")
setenv("F77", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/bin/pgfortran")
setenv("FC", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/bin/pgfortran")
prepend_path("PATH", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/bin", ":")
prepend_path("LD_LIBRARY_PATH", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/lib", ":")
prepend_path("MANPATH", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg/linuxpower/20.1/man", ":")
setenv("OLCF_PGI_ROOT", "/sw/peak/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-8-os/pgi-20.1-hspkmxwgxlwxvokyeitaexn2elv5qqfg")
prepend_path("MODULEPATH", "/sw/peak/modulefiles/site/linux-rhel7-ppc64le/pgi-extensions", ":")

