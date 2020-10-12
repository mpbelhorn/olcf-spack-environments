-- Internal variables
local base  = "/sw/sources/lsf-tools/"
local host = "summit"

-- Alter existing variables
prepend_path {"PATH", pathJoin(base, host, "bin"), priority=9999}

-- Info
help([[
LSF helper tools
]])

whatis("LSF helper tools")


