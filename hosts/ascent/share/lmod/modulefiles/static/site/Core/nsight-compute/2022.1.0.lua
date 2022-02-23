local host    = "ascent"
local version = "2022.1.0"
local pkg     = "nsight-compute"
local prefix  = pathJoin("/sw", host, pkg, version)

-- Info
help([[
Tools to use Nsight Compute
Version ]] .. version
)
whatis("Nvidia Nsight Compute")

-- Paths
prepend_path{"PATH", prefix, priority=9999}
setenv("OLCF_NSIGHT_COMPUTE_ROOT", prefix) 
