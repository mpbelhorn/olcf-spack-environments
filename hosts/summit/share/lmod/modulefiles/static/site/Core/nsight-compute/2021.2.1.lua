local host    = "summit"
local version = "2021.2.1"
local pkg     = "nsight-compute"
local prefix  = pathJoin("/sw", host, pkg, version)

-- Info
help([[
Tools to use Nsight Compute
Version ]] .. version
)
whatis("Nvidia Nsight Compute")

-- Paths
prepend_path{"PATH", pathJoin(prefix, "bin"), priority=9999}
setenv("OLCF_NSIGHT_COMPUTE_ROOT", prefix) 
