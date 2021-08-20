-- Internal variables
local base    = "/sw/sources/lsf-tools/"
local version = "2.0"
local system  = "summit"

-- Alter existing variables
prepend_path {"PATH", pathJoin(base, version, system, "bin"), priority=9999}

-- Info
help([[
LSF helper tools
]])

whatis("LSF helper tools")


