family("compiler")

-- Required internal variables
local package = "llvm"
local version = "9.0.1"
local package_spack = "clang"
local version_spack = "9.0.1"
local prefix = "/sw/andes/llvm/9.0.1/9.0.1-0"
local platform = 'linux-rhel8-x86_64'

local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, package_spack, version_spack)

-- The path to the gcc toolchain must be passed to clang either as
-- 1. export COMPILER_PATH=${gcc_toolchain}
-- 2. --gcc-toolchain=${gcc_toolchain}
-- Check with clang -v
local c_include_path = prefix .. "/include"
local cplus_include_path = prefix .. "/include"
local library_path = prefix .. "/lib:" .. prefix .. "/lib/clang/9.0.1/lib/linux:" .. prefix .. "/lib64"

--- List prerequisite modules here

-- Required for "module help ..."

help([[
Description - LLVM is a compiler infrastructure designed for compile-time, link-time, runtime, and idle-time optimization of programs from arbitrary programming languages.
Docs - https://llvm.org

"clang -Ofast test.c -o test"
]])

-- Required for "module display ..."
whatis("Description: ", "LLVM is a compiler infrastructure designed for compile-time, link-time, runtime, and idle-time optimization of programs from arbitrary programming languages.")

prepend_path( "MODULEPATH", spack_modules)

-- Software-specific settings exported to user environment
prepend_path("PATH", pathJoin(prefix, "bin"))
prepend_path("MANPATH", pathJoin(prefix, "share", "man"))
prepend_path("LIBRARY_PATH", library_path)
prepend_path("LD_LIBRARY_PATH", library_path)
prepend_path("CMAKE_PREFIX_PATH", prefix)
prepend_path("C_INCLUDE_PATH", c_include_path)
prepend_path("CPLUS_INCLUDE_PATH", cplus_include_path)

setenv("COMPILER_PATH", prefix)
setenv("LLVM_ROOT", prefix)
setenv("LLVM_VERSION", version)
setenv("OLCF_LLVM_ROOT", prefix)
