family("compiler")

help([[
AMD AOCC Compiler
]])


local package = "aocc"
local version = "2.1.0"
local prefix = "/sw/andes/aocc/2.1.0/aocc-compiler-2.1.0"
local platform = 'linux-rhel8-x86_64'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, 'clang/9.0.0-aocc2.1.0')

whatis("Description: ", "AMD AOCC EPYC Optimizing compiler " .. version)

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

-- Environment Globals
prepend_path( "PATH",  pathJoin(prefix, "bin" ) )
-- prepend_path( "MANPATH", pathJoin(gccdir, "share/man" ) )
prepend_path("LIBRARY_PATH", pathJoin(prefix, "lib32"))
prepend_path("LIBRARY_PATH", pathJoin(prefix, "lib"))
prepend_path("LIBRARY_PATH", "/usr/lib64:/usr/lib")
prepend_path("LD_LIBRARY_PATH", pathJoin(prefix, "lib32"))
prepend_path("LD_LIBRARY_PATH", pathJoin(prefix, "lib"))
prepend_path("LD_LIBRARY_PATH", "/usr/lib64:/usr/lib")
prepend_path("C_INCLUDE_PATH", pathJoin(prefix, "include"))
prepend_path("CPLUS_INCLUDE_PATH", pathJoin(prefix, "include"))

-- OLCF specific Environment
setenv("OLCF_AOCC_ROOT",  prefix)

