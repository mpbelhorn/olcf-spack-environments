-- family("compiler")

local host = "peak"
local package = "nvhpc_sdk"
local version = "21.7"
local target = "Linux_ppc64le"
local platform = 'linux-rhel8-ppc64le'
local nvhome = pathJoin("/sw", host, package, "rhel8")

-- local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
-- local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

local prefix = pathJoin(nvhome, target, version)
local nvcudadir = pathJoin(prefix, "cuda")
local nvcompdir = pathJoin(prefix, "compilers")
local nvmathdir = pathJoin(prefix, "math_libs")
local nvcommdir = pathJoin(prefix, "comm_libs")

setenv("NVHPC", nvhome)
--setenv("CC", pathJoin(nvcompdir, "bin", "nvc")
--setenv("CXX", pathJoin(nvcompdir, "bin", "nvc++")
--setenv("FC", pathJoin(nvcompdir, "bin", "nvfortran")
--setenv("F90", pathJoin(nvcompdir, "bin", "nvfortran")
--setenv("F77", pathJoin(nvcompdir, "bin", "nvfortran")
--setenv("CPP", "cpp")

prepend_path("PATH", pathJoin(nvcudadir, "bin"))
-- prepend_path("PATH", pathJoin(nvcompdir, "bin")

prepend_path("LD_LIBRARY_PATH", pathJoin(nvcudadir, "lib64"))
-- prepend_path("LD_LIBRARY_PATH", pathJoin(nvcompdir, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(nvmathdir, "lib64"))
prepend_path("LD_LIBRARY_PATH", pathJoin(nvcommdir, "nccl/lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(nvcommdir, "nvshmem/lib"))

prepend_path("CPATH", pathJoin(nvcudadir, "include"))
prepend_path("CPATH", pathJoin(nvmathdir, "include"))
prepend_path("CPATH", pathJoin(nvcommdir, "nccl/include"))
prepend_path("CPATH", pathJoin(nvcommdir, "nvshmem/include"))

prepend_path("MANPATH", pathJoin(nvcompdir, "man"))

setenv("OLCF_NVHPC_ROOT", prefix)

-- nvhpc provides it's own cuda toolkit. This should be implicitly used by default.
-- To do this, we replace the default cuda toolkit module with a blank
-- placeholder. Users can then reload an alternate cuda toolkit as desired.
prepend_path("MODULEPATH", pathJoin(nvhome, 'site-modulefiles'))
always_load("cuda/nvhpc")
