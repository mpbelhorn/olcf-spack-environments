family("compiler")

help([[
System GCC Compiler
]])

whatis("Description: ", "GCC compiler 4.8.5")

local package = "gcc"
local version = "4.8.5"
local platform = 'linux-rhel7-ppc64le'

local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

-- Environment Globals
--prepend_path( "PATH",  pathJoin(pgidir, "bin" ) )
--prepend_path( "MANPATH", pathJoin(pgidir, "man" ) )
--prepend_path( "LD_LIBRARY_PATH", pathJoin(pgidir, "lib") )

-- OLCF specific Environment
setenv("OLCF_GCC_ROOT",  "/usr")
