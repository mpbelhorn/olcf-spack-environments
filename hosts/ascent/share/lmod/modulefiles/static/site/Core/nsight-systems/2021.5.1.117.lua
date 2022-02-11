local host    = "ascent"
local version = "2021.5.1.117"
local pkg     = "nsight-systems"
local prefix  = pathJoin("/sw", host, pkg, version)

-- Info
help([[
Tools to use Nvidia Nsight Systems
Version ]] .. version
)
whatis("Nvidia Nsight Systems")

-- Paths
prepend_path{"PATH", pathJoin(prefix, "bin"), priority=100}
setenv("OLCF_NSIGHT_SYSTEMS_ROOT", prefix) 

