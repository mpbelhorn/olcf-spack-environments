-- -*- lua -*-

local host = "summit"
local anaconda_flavor = "anaconda3"
local py_version = "3.7"
local anaconda_version = "2020.07"
local prefix = pathJoin(
    "/sw", host, "python", py_version,  
    anaconda_flavor, anaconda_version .. "-rhel8")

whatis([[Name : python-]] .. anaconda_flavor)
whatis([[Anaconda Version : ]] .. anaconda_version)
whatis([[Python Version : ]] .. py_version)
whatis([[Short description : The Anaconda Python distribution.]])

help([[The Anaconda Python distribution.]])

prepend_path("PATH", pathJoin(prefix, "bin"), ":")
prepend_path("MANPATH", pathJoin(prefix, "share/man"), ":")
-- prepend_path("LD_LIBRARY_PATH", "", ":")
-- prepend_path("LIBRARY_PATH", "", ":")
-- prepend_path("CPATH", "", ":")

-- This might be useful...
-- prepend_path("PKG_CONFIG_PATH", prefix .. "lib/pkgconfig", ":")
-- prepend_path("CMAKE_PREFIX_PATH", "", ":")

unsetenv("PYTHONSTARTUP")

local user_home = os.getenv("HOME") or ""
if (user_home ~= "") then
  setenv("PYTHONUSERBASE",
         pathJoin(user_home, ".local", host, anaconda_flavor, anaconda_version,
                  py_version)
        )
end

setenv("OLCF_PYTHON_" .. anaconda_flavor:upper() .. "_ROOT", prefix)


