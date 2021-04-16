family("compiler")

help([[
AMD AOCC Compiler
]])


local package = "aocc"
local version = "2.3.0"
local prefix = pathJoin("/sw/andes/aocc", version, "/aocc-compiler-" .. version)
local platform = 'linux-rhel8-x86_64'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

whatis("Description: ", "AMD AOCC EPYC Optimizing compiler " .. version)

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

-- Environment Globals
prepend_path( "PATH",  pathJoin(prefix, "bin" ) )

append_path("LD_LIBRARY_PATH", pathJoin(prefix, "lib"))
append_path("LD_LIBRARY_PATH", pathJoin(prefix, "lib32"))
-- prepend_path("LD_LIBRARY_PATH", "/usr/lib64:/usr/lib")

append_path("LIBRARY_PATH", pathJoin(prefix, "lib"))
append_path("LIBRARY_PATH", pathJoin(prefix, "lib32"))
-- prepend_path("LIBRARY_PATH", "/usr/lib64:/usr/lib")

append_path("C_INCLUDE_PATH", pathJoin(prefix, "include"))
append_path("CPLUS_INCLUDE_PATH", pathJoin(prefix, "include"))

-- prepend_path( "MANPATH", pathJoin(gccdir, "share/man" ) )

-- OLCF specific Environment
setenv("OLCF_AOCC_ROOT",  prefix)
