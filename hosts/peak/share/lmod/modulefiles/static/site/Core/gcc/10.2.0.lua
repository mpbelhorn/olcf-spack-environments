family("compiler")

help([[
GCC Compiler
]])


local package = "gcc"
local version = "10.2.0"
local host = "peak"
local gccdir = pathJoin("/sw", host, "gcc/10.2.0-2")
local platform = 'linux-rhel8-ppc64le'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

whatis("Description: ", "GCC compiler " .. version)

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

-- Environment Globals
prepend_path( "PATH",  pathJoin(gccdir, "bin" ) )
prepend_path( "MANPATH", pathJoin(gccdir, "share/man" ) )
prepend_path( "LD_LIBRARY_PATH", pathJoin(gccdir, "lib64") )

-- OLCF specific Environment
setenv("OLCF_GCC_ROOT",  gccdir)
