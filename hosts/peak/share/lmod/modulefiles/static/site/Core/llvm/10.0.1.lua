family("compiler")

-- Required internal variables
local package = "llvm"
local version = "10.0.1"
local package_spack = "clang"
local version_spack = "10.0.1-0"
local prefix = "/sw/peak/llvm/10.0.1/10.0.1-0"

local platform = 'linux-rhel8-ppc64le'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, package_spack, version_spack)

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)

-- The path to the gcc toolchain must be passed to clang either as
-- 1. export COMPILER_PATH=${gcc_toolchain}
-- 2. --gcc-toolchain=${gcc_toolchain}
-- Check with clang -v
local gcc_toolchain = "/usr"
local c_include_path = pathJoin(prefix, "include")
local cplus_include_path = pathJoin(prefix, "include")
local library_path = pathJoin(prefix, "lib") .. ":" .. pathJoin(prefix, "lib/clang", version, "lib/linux")

-- Required for "module help ..."

help([[
Description - LLVM is a compiler infrastructure designed for compile-time, link-time, runtime, and idle-time optimization of programs from arbitrary programming languages.
Docs - https://llvm.org

"clang -Ofast test.c -o test"
]])

-- Required for "module display ..."
whatis("Description: ", "LLVM is a compiler infrastructure designed for compile-time, link-time, runtime, and idle-time optimization of programs from arbitrary programming languages.")

-- Software-specific settings exported to user environment
prepend_path("PATH", pathJoin(prefix, "bin"))
prepend_path("MANPATH", pathJoin(prefix, "share", "man"))
prepend_path("LIBRARY_PATH", library_path)
prepend_path("LD_LIBRARY_PATH", library_path)
prepend_path("CMAKE_PREFIX_PATH", prefix)
prepend_path("C_INCLUDE_PATH", c_include_path)
prepend_path("CPLUS_INCLUDE_PATH", cplus_include_path)

setenv("COMPILER_PATH", gcc_toolchain)
setenv("LLVM_ROOT", prefix)
setenv("LLVM_VERSION", version)
setenv("OLCF_LLVM_ROOT", prefix)
