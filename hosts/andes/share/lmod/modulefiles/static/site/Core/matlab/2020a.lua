-- -*- lua -*-

whatis([[Name : matlab]])
whatis([[Version : R2020a]])
whatis([[Short description : MATLAB (MATrix LABoratory) is a multi-paradigm numerical computing environment and fourth-generation programming language. A proprietary programming language developed by MathWorks, MATLAB allows matrix manipulations, plotting of functions and data, implementation of algorithms, creation of user interfaces, and interfacing with programs written in other languages, including C, C++, C#, Java, Fortran and Python.]])

help([[MATLAB (MATrix LABoratory) is a multi-paradigm numerical computing
environment and fourth-generation programming language. A proprietary
programming language developed by MathWorks, MATLAB allows matrix
manipulations, plotting of functions and data, implementation of
algorithms, creation of user interfaces, and interfacing with programs
written in other languages, including C, C++, C#, Java, Fortran and
Python.]])


prepend_path("PATH", "/sw/andes/matlab/R2020a/bin", ":")
prepend_path("CMAKE_PREFIX_PATH", "/sw/andes/matlab/R2020a", ":")
setenv("OLCF_MATLAB_ROOT", "/sw/andes/matlab/R2020a")

