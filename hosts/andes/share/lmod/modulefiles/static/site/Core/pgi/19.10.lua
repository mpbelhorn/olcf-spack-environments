whatis([[Name : pgi]])
whatis([[Version : 19.10]])
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

local platform = 'linux-rhel8-x86_64'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

prepend_path("CMAKE_PREFIX_PATH", "/sw/andes/pgi/19.10/", ":")
setenv("CC", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/bin/pgcc")
setenv("CXX", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/bin/pgc++")
setenv("F77", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/bin/pgfortran")
setenv("FC", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/bin/pgfortran")
prepend_path("PATH", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/bin", ":")
prepend_path("LD_LIBRARY_PATH", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/lib", ":")
prepend_path("MANPATH", "/sw/andes/pgi/19.10/linux86-64-llvm/19.10/man", ":")
setenv("OLCF_PGI_ROOT", "/sw/andes/pgi/19.10/")
-- prepend_path("MODULEPATH", "/sw/andes/modulefiles/pgi-extensions", ":")

