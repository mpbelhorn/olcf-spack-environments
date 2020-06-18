-- -*- lua -*-
-- Module file created by spack (https://github.com/spack/spack) on 2019-09-17 12:39:39.266451
--
-- pgi@18.10%gcc@4.8.5~amd~java+managed+mpi+mpigpu~network+nvidia+single arch=linux-rhel7-ppc64le /w2qkfai
--

whatis([[Name : pgi]])
whatis([[Version : 18.10]])
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

local platform = 'linux-rhel7-ppc64le'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

prepend_path("CMAKE_PREFIX_PATH", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/", ":")
setenv("CC", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/bin/pgcc")
setenv("CXX", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/bin/pgc++")
setenv("F77", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/bin/pgfortran")
setenv("FC", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/bin/pgfortran")
prepend_path("PATH", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/bin", ":")
prepend_path("LD_LIBRARY_PATH", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/lib", ":")
prepend_path("MANPATH", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur/linuxpower/18.10/man", ":")
setenv("OLCF_PGI_ROOT", "/autofs/nccs-svm1_sw/peak/.swci/0-core/opt/spack/20180914/linux-rhel7-ppc64le/gcc-4.8.5/pgi-18.10-w2qkfaill2olnyrfykr5a3kmwaz6pjur")
prepend_path("MODULEPATH", "/sw/peak/modulefiles/site/linux-rhel7-ppc64le/pgi-extensions", ":")

