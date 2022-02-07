-- -*- lua -*-

local package = "cuda"
local version = "10.1.168"
local host = "ascent"
local prefix = pathJoin("/sw", host, package, version)

whatis([[Changes the CUDA module]])
help([[ Tools to use CUDA

        Version ]] .. version .. [[

]])

try_load("nsight-compute", "nsight-systems")
prepend_path("PATH", pathJoin(prefix, "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(prefix, "lib64"))
prepend_path("MANPATH", pathJoin(prefix, "doc/man"))
prepend_path("CPATH", pathJoin(prefix, "include"))
setenv("CUDA_DIR", prefix)
setenv("CUDA_TOOLKIT_ROOT_DIR", prefix)
setenv("OLCF_CUDA_ROOT", prefix)
setenv("CUDAPATH", prefix)
setenv("CUDA_PATH", prefix)
