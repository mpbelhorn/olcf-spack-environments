whatis([[Name : intel]])
whatis([[Version : 2021.4.0]])
help([[The Intel oneAPI Compiler Suite]])

-- Internal variables
local swroot  = "/sw/andes/intel/21.4.0"
local version = "2021.4.0"
local platform = 'linux-rhel8-x86_64'
local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Package family
family("compiler")

-- Setup Modulepath for packages built by this compiler
---- use only one version sublevel
prepend_path( "MODULEPATH", spack_modules)

-- Setup center variables
setenv("OLCF_INTEL_ROOT",  swroot)

-- Compiler Paths
-- Elements in reverse order of priority.
local compiler_root = pathJoin(swroot, "compiler", version, "linux")
append_path("OCL_ICD_FILENAMES", pathJoin(compiler_root, "lib/x64/libintelocl.so"))
prepend_path("PATH", pathJoin(compiler_root, "bin"))
prepend_path("PATH", pathJoin(compiler_root, "bin", "intel64"))
prepend_path("CPATH", pathJoin(compiler_root, "include"))
prepend_path("LIBRARY_PATH", pathJoin(compiler_root, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(compiler_root, "compiler/lib/intel64_lin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(compiler_root, "lib/emu"))
prepend_path("LD_LIBRARY_PATH", pathJoin(compiler_root, "lib/x64"))
prepend_path("LD_LIBRARY_PATH", pathJoin(compiler_root, "lib"))
prepend_path("MANPATH", pathJoin(swroot, "compiler", version, "documentation/en/man/common"))

local tbb_root = pathJoin(swroot, "tbb", version)
setenv(                "TBBROOT", tbb_root)
prepend_path("CMAKE_PREFIX_PATH", tbb_root)
prepend_path(            "CPATH", pathJoin(tbb_root, "include"))
prepend_path(     "LIBRARY_PATH", pathJoin(tbb_root, "lib/intel64/gcc4.8"))
prepend_path(  "LD_LIBRARY_PATH", pathJoin(tbb_root, "lib/intel64/gcc4.8"))

local dpl_root = pathJoin(swroot, "dpl", "2021.5.0")
setenv(   "DPL_ROOT", dpl_root)
prepend_path("CPATH", pathJoin(dpl_root, "linux", "include"))

local mkl_root = pathJoin(swroot, "mkl", version)
setenv(              "MKLROOT", mkl_root)
prepend_path(          "CPATH", pathJoin(mkl_root, "include"))
prepend_path(   "LIBRARY_PATH", pathJoin(mkl_root, "lib/intel64"))
prepend_path("LD_LIBRARY_PATH", pathJoin(mkl_root, "lib/intel64"))
prepend_path("PKG_CONFIG_PATH", pathJoin(mkl_root, "lib/pkgconfig"))
prepend_path(        "NLSPATH", pathJoin(mkl_root, "lib/intel64/locale/%l_%t/%N"))

local ipp_root = pathJoin(swroot, "ipp", version)
setenv("IPPROOT", ipp_root)
setenv("IPP_TARGET_ARCH", "intel64")
prepend_path(            "CPATH", pathJoin(ipp_root, "include"))
prepend_path(     "LIBRARY_PATH", pathJoin(ipp_root, "lib/intel64"))
prepend_path(  "LD_LIBRARY_PATH", pathJoin(ipp_root, "lib/intel64"))
