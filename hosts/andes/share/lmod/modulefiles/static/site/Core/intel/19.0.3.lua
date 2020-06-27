whatis([[Name : intel]])
whatis([[Version : 19.0.3]])
help([[The Intel Compiler Suite and Parallel Studio XE including MKL.]])

-- Internal variables
local swroot  = "/sw/andes/intel/19.0.3"
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
prepend_path("LD_LIBRARY_PATH", pathJoin(swroot, "tbb/lib/intel64/gcc4.7"))
prepend_path("LD_LIBRARY_PATH", pathJoin(swroot, "mkl/lib/intel64"))
prepend_path("LD_LIBRARY_PATH", pathJoin(swroot, "ipp/lib/intel64"))
prepend_path("LD_LIBRARY_PATH", pathJoin(swroot, "lib/intel64"))

prepend_path("MANPATH", pathJoin(swroot, "man/common"))

prepend_path("PATH", pathJoin(swroot, "debugger_2019/gdb/intel64/bin"))
prepend_path("PATH", pathJoin(swroot, "bin"))

prepend_path("NLSPATH", pathJoin(swroot, "debugger_2019/gdb/intel64/share/locale/%l/LC_MESSAGES/%N"))
prepend_path("NLSPATH", pathJoin(swroot, "mlk/lib/intel64/locale/%l_%t/%N"))
prepend_path("NLSPATH", pathJoin(swroot, "lib/intel64/locale/%l_%t/%N"))

--Static envvars
setenv("MKLROOT", pathJoin(swroot, "mkl"))
setenv("IPPROOT", pathJoin(swroot, "ipp"))
setenv("TBBROOT", pathJoin(swroot, "tbb"))
setenv("IDB_HOME", pathJoin(swroot, "bin"))
setenv("INTEL_LICENSE_FILE", "7136@flex1.ccs.ornl.gov:7136@flex2.ccs.ornl.gov:7136@flex3.ccs.ornl.gov")
