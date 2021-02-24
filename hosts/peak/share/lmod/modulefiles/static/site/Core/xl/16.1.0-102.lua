-- Package family
family("compiler")

-- Internal variables
local swroot  = "/sw/peak/xl/16.1.0-102"
local xlfbase    = pathJoin(swroot, "xlf", "16.1.0")
local xlcbase    = pathJoin(swroot, "xlC", "16.1.0")
local xlmassbase = pathJoin(swroot, "xlmass", "9.1.0")
local xlsmpbase  = pathJoin(swroot, "xlsmp", "5.1.0")

local platform = 'linux-rhel8-ppc64le'
-- local spack_module_root, _ = myFileName():gsub('/site/Core/'..myModuleFullName()..'.*', '/spack')
local spack_module_root = (myFileName():sub(1, myFileName():find(myModuleFullName(),1,true)-2)):gsub("/site/Core.*",'/spack')
local spack_modules = pathJoin(spack_module_root, platform, myModuleFullName())

-- Setup Modulepath for packages built by this compiler
prepend_path( "MODULEPATH", spack_modules)


-- Setup center variables
setenv("OLCF_XL_ROOT",     swroot)
setenv("OLCF_XLF_ROOT",    xlfbase)
setenv("OLCF_XLC_ROOT",    xlcbase)
setenv("OLCF_XLMASS_ROOT", xlmassbase)
setenv("OLCF_XLSMP_ROOT",  xlsmpbase)


-- Alter existing variables
prepend_path( "LD_LIBRARY_PATH", pathJoin (swroot, "lib") )
prepend_path( "NLSPATH",         pathJoin (swroot, "msg/en_US/%N") )

prepend_path( "PATH",            pathJoin(xlfbase, "bin") )
prepend_path( "MANPATH",         pathJoin(xlfbase, "man/en_US" ) )
prepend_path( "LD_LIBRARY_PATH", pathJoin(xlfbase, "lib") )
prepend_path( "NLSPATH",         pathJoin(xlfbase, "msg/en_US/%N") )

prepend_path( "PATH",            pathJoin(xlcbase, "bin") )
prepend_path( "MANPATH",         pathJoin(xlcbase, "man/en_US" ) )
prepend_path( "LD_LIBRARY_PATH", pathJoin(xlcbase, "lib") )
prepend_path( "NLSPATH",         pathJoin(xlcbase, "msg/en_US/%N") )

prepend_path( "LD_LIBRARY_PATH", pathJoin(xlmassbase, "lib") )
prepend_path( "LD_LIBRARY_PATH", pathJoin(xlsmpbase,  "lib") )

prepend_path( "NLSPATH", pathJoin( swroot, "msg", "en_US", "%N"  ) )

-- Info
help([[
xlc version: 16.1.0-beta102
xlf version: 16.1.0-beta102
xlmass version: 9.1.0-beta102
xlsmp version: 5.1.0-beta102
]])

whatis("Description: xlc 16.1.0-beta102, xlf 16.1.0-beta102, xlmass 9.1.0-beta102, xlsmp 5.1.0-beta102")

