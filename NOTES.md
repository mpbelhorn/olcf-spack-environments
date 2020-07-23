# Lessons Learned and Best Practices

- Specs for large `defnitions:` sets of target applications that should be built with each
    compiler should be expressed as a separate matrix for each compiler class to
    more easily exclude problem builds and include more verbose exceptional
    specs near the block in which packages are handled for a given class of
    toolchain. IE:
    ```
    - matrix:
      - - $general_compute_packages
      - - $gcc_compilers
      exclude:
      - 'amgx%gcc@9:'
    - hpx %gcc@8.1.1 cxxstd=14 ^boost@1.70.0
    - hpx %gcc@8.1.1 cxxstd=17 ^boost@1.70.0
    - matrix:
      - - $general_compute_packages
      - - $llvm_compilers
      - - arch=linux-rhel7-power9le
      - - ^elfutils%gcc@4.8.5 arch=linux-rhel7-power8le
    - matrix:
      - - $general_compute_packages
      - - $xl_compilers
      - - arch=linux-rhel7-power9le
      - - ^numactl%gcc@4.8.5 arch=linux-rhel7-power8le
      exclude:
      - boost@1.63.0:%xl
    ```
    is better than:
    ```
    - matrix:
      - - $general_compute_packages
      - - $all_compilers
      exclude:
      # lots of exceptions and separate matrixes for problem builds.
    ```
    This way, specs for a given package that needs to be done differently for
    each toolchain are not widely spread out across the manifest. This also
    allows deployment of the whole stack for compiler classes that can do all
    the builds reliably sooner than the tricky edge cases. Ie, we'll always have
    at least one compiler environment that has everything.

# Build Problems

## Spack bugs

- Changes to a preferred package version in an environment does not get applied
    when concretizing matrix specs without `spack concretize -f`.

## Andes

- rdma-core with intel compilers:
  The path set via `buildlib/config.h.in` for `#define ACM_CONF_DIR "@CMAKE_INSTALL_FULL_SYSCONFDIR@/rdma"` can be exceptionally long under spack.
  For example, in file `ibacm/prov/acmp/src/acmp.c`, the line (274) `static char route_data_file[128] = ACM_CONF_DIR "/ibacm_route.data";` sets a string 134+
  characters long (ie `len("/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/clang-9.0.1/rdma-core-28.0-2ixcucck7eb4fzbd3t6imjrhz5qahxui/etc/rdma/ibacm_route.data")`).

  This causes the intel comppilers to choke when trying to shove that string
  into a 128-character array. Patching the source code to allow for a path up to
  192 characters in length lets the build succeed, but I do not know if this
  breaks other things.
- AOCC 2.2.0 (and possibly earlier) has issues with OMP and some expected GCC
  math libraries if using the build of flang provided by the module when
  building with spack. For example, building HDF5:
  ```
  /autofs/nccs-svm1_sw/.testing/belhorn/spack/facility-spack/spack/lib/spack/env/clang/flang  -I. -I../../src -I../../fortran/src     -I../../fortran/src -I../../fortran/src -fPIC -c -o fortranlib_test.o fortranlib_test.F90
    FCLD     fortranlib_test
  ld.lld: error: undefined symbol: fabsq
  >>> referenced by tf_gen.F90:172
  >>>               tf_gen.o:(th5_misc_gen_real_eq_kind_16_) in archive ./.libs/libh5test_fortran.a
  >>> referenced by tf_gen.F90:172
  >>>               tf_gen.o:(th5_misc_gen_real_eq_kind_16_) in archive ./.libs/libh5test_fortran.a
  >>> referenced by tf_gen.F90:172
  >>>               tf_gen.o:(th5_misc_gen_real_eq_kind_16_) in archive ./.libs/libh5test_fortran.a
  >>> did you mean: fabsf
  >>> defined in: /lib64/libm.so.6

  ld.lld: error: undefined symbol: fmaxq
  >>> referenced by tf_gen.F90:172
  >>>               tf_gen.o:(th5_misc_gen_real_eq_kind_16_) in archive ./.libs/libh5test_fortran.a
  clang-10: error: linker command failed with exit code 1 (use -v to see invocation)
  make[2]: *** [Makefile:931: fortranlib_test] Error 1
  make[2]: Leaving directory '/run/user/12126/belhorn/spack-stage-hdf5-1.10.6-gt27bq6cih6futelz3i3tekfwylx52t7/spack-src/fortran/test'
  make[1]: *** [Makefile:820: all-recursive] Error 1
  make[1]: Leaving directory '/run/user/12126/belhorn/spack-stage-hdf5-1.10.6-gt27bq6cih6futelz3i3tekfwylx52t7/spack-src/fortran'
  make: *** [Makefile:660: all-recursive] Error 1
  ```
- mfem fails to build due to following error in simple build case:
```
==> Error: Failed to install mfem due to ChildError: ProcessError: Command exited with status 2:                                                                                                                                               
    'make' '-j16' 'lib'                                                                                                                                                                                                                        
1 error found in build log:                                                                                                                                                                                                                    
     106    /sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/openmpi-4.0.4-wfz3nk67jzegocblvwhtmqjjqel                                                                                                                               
            ridk5/bin/mpic++   -O3 -std=c++11 -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/hypre                                                                                                                               
            -2.18.0-bammqydlgzcntddviulb6ndoixfwyg4h/include -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/       
            gcc-8.3.1/metis-5.1.0-ahuci2nwesonop73arnq5uzvsyxnwsy4/include -I/sw/andes/spack-envs/base/opt/linux       
            -rhel8-x86_64/gcc-8.3.1/zlib-1.2.11-xqjeqtupcfqqqlaw5ehjlfjjly7zoe3b/include  -c linalg/sundials.cpp       
             -o linalg/sundials.o                          
     107    /sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/openmpi-4.0.4-wfz3nk67jzegocblvwhtmqjjqel       
            ridk5/bin/mpic++   -O3 -std=c++11 -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/hypre       
            -2.18.0-bammqydlgzcntddviulb6ndoixfwyg4h/include -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/       
            gcc-8.3.1/metis-5.1.0-ahuci2nwesonop73arnq5uzvsyxnwsy4/include -I/sw/andes/spack-envs/base/opt/linux       
            -rhel8-x86_64/gcc-8.3.1/zlib-1.2.11-xqjeqtupcfqqqlaw5ehjlfjjly7zoe3b/include  -c linalg/ode.cpp -o l       
            inalg/ode.o                                    
     108    /sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/openmpi-4.0.4-wfz3nk67jzegocblvwhtmqjjqel       
            ridk5/bin/mpic++   -O3 -std=c++11 -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/hypre       
            -2.18.0-bammqydlgzcntddviulb6ndoixfwyg4h/include -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/       
            gcc-8.3.1/metis-5.1.0-ahuci2nwesonop73arnq5uzvsyxnwsy4/include -I/sw/andes/spack-envs/base/opt/linux       
            -rhel8-x86_64/gcc-8.3.1/zlib-1.2.11-xqjeqtupcfqqqlaw5ehjlfjjly7zoe3b/include  -c linalg/hiop.cpp -o        
            linalg/hiop.o                                  
     109    /sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/openmpi-4.0.4-wfz3nk67jzegocblvwhtmqjjqel       
            ridk5/bin/mpic++   -O3 -std=c++11 -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/hypre       
            -2.18.0-bammqydlgzcntddviulb6ndoixfwyg4h/include -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/       
            gcc-8.3.1/metis-5.1.0-ahuci2nwesonop73arnq5uzvsyxnwsy4/include -I/sw/andes/spack-envs/base/opt/linux       
            -rhel8-x86_64/gcc-8.3.1/zlib-1.2.11-xqjeqtupcfqqqlaw5ehjlfjjly7zoe3b/include  -c linalg/superlu.cpp        
            -o linalg/superlu.o                            
     110    /sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/openmpi-4.0.4-wfz3nk67jzegocblvwhtmqjjqel       
            ridk5/bin/mpic++   -O3 -std=c++11 -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/gcc-8.3.1/hypre       
            -2.18.0-bammqydlgzcntddviulb6ndoixfwyg4h/include -I/sw/andes/spack-envs/base/opt/linux-rhel8-x86_64/       
            gcc-8.3.1/metis-5.1.0-ahuci2nwesonop73arnq5uzvsyxnwsy4/include -I/sw/andes/spack-envs/base/opt/linux       
            -rhel8-x86_64/gcc-8.3.1/zlib-1.2.11-xqjeqtupcfqqqlaw5ehjlfjjly7zoe3b/include  -c linalg/solvers.cpp        
            -o linalg/solvers.o                            
     111    linalg/hypre.cpp: In copy constructor 'mfem::HypreParMatrix::HypreParMatrix(const mfem::HypreParMatr       
            ix&)':                                         
  >> 112    linalg/hypre.cpp:822:8: error: 'hypre_ParCSRMatrixCompleteClone' was not declared in this scope            
     113        A = hypre_ParCSRMatrixCompleteClone(Ph);                                                               
     114            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
     115    linalg/hypre.cpp:822:8: note: suggested alternative: 'hypre_ParCSRMatrixClone'                             
     116        A = hypre_ParCSRMatrixCompleteClone(Ph);                                                               
     117            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
     118            hypre_ParCSRMatrixClone     
```

## Peak

- raja@0.5.3%gcc@8.1.1 on peak: `__ieee128` C++ error.
- papi: filter_file over `**/*.[ch]` hangs on random files.
- `netcdf-fortran%xl`: libtool calls do not include `-L` arguments for
    `Spec('netcdf)['hdf5']` libraries despite those paths being in
    `SPACK_LINK_DIRS` and `SPACK_RPATH_DIRS`
  - Solution(?): enforce hdf5 dependency when building with xl?
- Using generic full anaconda installation to provide base python exposes
    unwanted tools from anaconda distro. For example:
    ```
    /sw/peak/python/3.7/anaconda3/5.3.0/bin/fc-cache /sw/.b2/envs/peak/base/opt/linux-rhel7-power8le/gcc-4.8.5/font-util-1.3.2-tdhbdp4kjq2rxokfsfn6giwzsr42greu/share/fonts/X11/cyrillic
    ```
- Linking against ZFP built with GCC >=6.4.0 fails to find the right libstdc++;
    probably a library search error when building zfp?

## IBM-specific problems

In spectrum-mpi-10.3.1.2-20200121-*/include/mpi.h:268:

```c
#if (1 == SMPI_HAVE_PRAGMA_WEAK)
   /*   
                    
    * test_version() is put into user's object files as
    * a weak symbol, so users can use a utility such as
    * strings to see what SMPI version it was built with.
    */
  #if defined(c_plusplus) || defined(__cplusplus)
    extern "C"
    {    
  #endif
      #pragma weak smpi_built_against_version
      OMPI_DECLSPEC const char * smpi_built_against_version(void);
      OMPI_DECLSPEC const char * smpi_built_against_version(void) { return "SMPI_BUILT_AGAINST_VERSION=" SMPI_VERSION_STR; }
  #if defined(c_plusplus) || defined(__cplusplus)
    } /* extern "C" */
  #endif
#endif
```

first declaration of `OMPI_DECLSPEC const char * smpi_built_against_version(void);` is redundant and problematic.

# Maintenance problems

- Unregistering packages from spack DB in an environment?
- Uninstalling package from env without removing it from env SpecList
  - No way to current remove specs expanded from a matrix, but sometimes there
    is a need to be rebuild such packages (along with their dependents).
  - Often want to remove modules for such packages as well, especially if module
      is initially for an "external" build.
  - Generally do not wish to change the spec list, just remove the old builds
      and modules.

- Matrix stacks of conflict builds should warn that a spec conflicts with a
    compiler but continue concretizing the env with allowed specs. For example,
    the following error should not be fatal:

  ```
  ==> Error: Conflicts in concretized spec "raja@0.8.0%gcc@4.8.5 build_type=RelWithDebInfo ~cuda+openmp arch=linux-rhel7-power8le/xymlav5"
  
  List of matching conflicts for spec:

      raja@0.8.0%gcc@4.8.5 build_type=RelWithDebInfo ~cuda+openmp arch=linux-rhel7-power8le
          ^cmake@3.16.2%gcc@4.8.5~doc+ncurses+openssl+ownlibs~qt arch=linux-rhel7-power8le
              ^ncurses@6.1%gcc@4.8.5~symlinks~termlib arch=linux-rhel7-power8le
                  ^pkgconf@1.6.3%gcc@4.8.5 arch=linux-rhel7-power8le
              ^openssl@1.0.2%gcc@4.8.5+systemcerts arch=linux-rhel7-power8le

  1. "%gcc@:4.999" conflicts with "raja@0.5:"
  ```
  for the matrix:
  ```
  - definitions:
    - gcc_compilers:
      - '%gcc@4.8.5'
      - '%gcc@6.4.0'
    - manifest:
      - matrix:
        - - raja
        - - $gcc_compilers
  ```

- Cannot `spack find` one-off specs, notably built with CLI cflags and fflags
    arguments.
  - `spec -lINt` shows them as installed, but `find` with either a hash argument
      or partial spec fails to find them.

- `blacklist_implicits: True` fails to publish any modulefiles for LMOD.

- deleted environment, but not lock file:
  ```
  $ spack -v -d find
  ==> [2020-02-03-10:30:13.053760] Imported find from built-in commands
  ==> [2020-02-03-10:30:13.054995] Imported find from built-in commands
  ==> [2020-02-03-10:30:13.055733] Reading config file /autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/var/spack/environments/test/spack.yaml
  Traceback (most recent call last):
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/bin/spack", line 64, in <module>
      sys.exit(spack.main.main())
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/lib/spack/spack/main.py", line 752, in main
      return _invoke_command(command, parser, args, unknown)
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/lib/spack/spack/main.py", line 486, in _invoke_command
      return_val = command(parser, args)
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/lib/spack/spack/cmd/find.py", line 203, in find
      results = args.specs(**q_args)
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/lib/spack/spack/cmd/common/arguments.py", line 75, in _specs
      kwargs['hashes'] = set(env.all_hashes())
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/lib/spack/spack/environment.py", line 1232, in all_hashes
      return list(self.all_specs_by_hash().keys())
    File "/autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/lib/spack/spack/environment.py", line 1221, in all_specs_by_hash
      specs = self.specs_by_hash[h].traverse(deptype=('link', 'run'))
  KeyError: 'gdd24gc5segaupqphgmu5bky4n4jxlai'

  $ grep gdd24gc5segaupqphgmu5bky4n4jxlai hosts/peak/spack/var/spack/environments/test/spack.lock                                                                                                                                                
   "hash": "gdd24gc5segaupqphgmu5bky4n4jxlai",
  "gdd24gc5segaupqphgmu5bky4n4jxlai": {
      "hash": "gdd24gc5segaupqphgmu5bky4n4jxlai",
      "hash": "gdd24gc5segaupqphgmu5bky4n4jxlai",

  ```

- package default variants do not pass thorugh environment concretization as
    expected. For example, `python` by default does not build with libxml2
    support and requests `gettext~libxml2` as a dependency. Gettext has
    `+libxml2` by default. The resulting error is:

    ```
    $ spack concretize
    # ....
    ==> Error: An unsatisfiable variant constraint has been detected for spec:
        gettext@0.20.1%gcc@4.8.5+bzip2+curses+git~libunistring+libxml2+tar+xz arch=linux-rhel7-power8le
            ^bzip2@1.0.8%gcc@4.8.5+shared arch=linux-rhel7-power8le
                ^diffutils@3.7%gcc@4.8.5 arch=linux-rhel7-power8le
                    ^libiconv@1.16%gcc@4.8.5 arch=linux-rhel7-power8le
            ^libxml2@2.9.9%gcc@4.8.5~python arch=linux-rhel7-power8le
                ^pkgconf@1.6.3%gcc@4.8.5 arch=linux-rhel7-power8le
                ^xz@5.2.4%gcc@4.8.5 arch=linux-rhel7-power8le
                ^zlib@1.2.11%gcc@4.8.5+optimize+pic+shared arch=linux-rhel7-power8le
            ^ncurses@6.1%gcc@4.8.5~symlinks~termlib arch=linux-rhel7-power8le
            ^tar@1.32%gcc@4.8.5 arch=linux-rhel7-power8le


    while trying to concretize the partial spec:

        python@3.7.0%gcc@4.8.5+bz2+ctypes+dbm~debug~libxml2+lzma~nis~optimizations+pic+pyexpat+pythoncmd+readline+shared+sqlite3+ssl~tix~tkinter~ucs4~uuid+zlib arch=linux-rhel7-power8le
            ^pkgconf@1.6.3%gcc@4.8.5 arch=linux-rhel7-power8le


    python requires gettext variant ~libxml2, but spec asked for +libxml2
    ```

    However, classical spec concretization still works:
    ```
    $ spack spec "python@3.7.0%gcc@4.8.5+bz2+ctypes+dbm~debug~libxml2+lzma~nis~optimizations+pic+pyexpat+pythoncmd+readline+shared+sqlite3+ssl~tix~tkinter~ucs4~uuid+zlib arch=linux-rhel7-power8le"                                               
    Input spec
    --------------------------------
    python@3.7.0%gcc@4.8.5+bz2+ctypes+dbm~debug~libxml2+lzma~nis~optimizations+pic+pyexpat+pythoncmd+readline+shared+sqlite3+ssl~tix~tkinter~ucs4~uuid+zlib arch=linux-rhel7-power8le

    Concretized
    --------------------------------
    ==> Warning: Using GCC 4.8 to optimize for Power 8 might not work if you are not on Red Hat Enterprise Linux 7, where a custom backport of the feature has been done. Upstream support from GCC starts in version 4.9
    python@3.7.0%gcc@4.8.5+bz2+ctypes+dbm~debug~libxml2+lzma~nis~optimizations+pic+pyexpat+pythoncmd+readline+shared+sqlite3+ssl~tix~tkinter~ucs4~uuid+zlib arch=linux-rhel7-power8le
        ^bzip2@1.0.8%gcc@4.8.5+shared arch=linux-rhel7-power8le
            ^diffutils@3.7%gcc@4.8.5 arch=linux-rhel7-power8le
                ^libiconv@1.16%gcc@4.8.5 arch=linux-rhel7-power8le
        ^expat@2.2.9%gcc@4.8.5+libbsd arch=linux-rhel7-power8le
            ^libbsd@0.10.0%gcc@4.8.5 arch=linux-rhel7-power8le
        ^gdbm@1.18.1%gcc@4.8.5 arch=linux-rhel7-power8le
            ^readline@8.0%gcc@4.8.5 arch=linux-rhel7-power8le
                ^ncurses@6.1%gcc@4.8.5~symlinks~termlib arch=linux-rhel7-power8le
                    ^pkgconf@1.6.3%gcc@4.8.5 arch=linux-rhel7-power8le
        ^gettext@0.20.1%gcc@4.8.5+bzip2+curses+git~libunistring~libxml2+tar+xz arch=linux-rhel7-power8le
            ^tar@1.32%gcc@4.8.5 arch=linux-rhel7-power8le
            ^xz@5.2.4%gcc@4.8.5 arch=linux-rhel7-power8le
        ^libffi@3.2.1%gcc@4.8.5 arch=linux-rhel7-power8le
        ^openssl@1.0.2%gcc@4.8.5+systemcerts arch=linux-rhel7-power8le
        ^sqlite@3.30.1%gcc@4.8.5~column_metadata+fts~functions~rtree arch=linux-rhel7-power8le
            ^zlib@1.2.11%gcc@4.8.5+optimize+pic+shared arch=linux-rhel7-power8le
    ```

- Fallback target microarchitecture should be most generic instead of most
    specific possible:
  ```
  Warning: gcc@4.8.5 cannot build optimized binaries for "power9le". Using best target possible: "power8le"
  ```
  I'd rather have this fallback to `ppc64le`. Setting package defaults in `spack.yaml` to:
  ```
    packages:
      # General Settings
      all:
        compiler: [gcc@4.8.5, gcc, clang, xl, pgi]
        providers:
          mpi: [olcf.spectrum-mpi]
          lapack: [netlib-lapack]
          blas: [netlib-lapack]
          scalapack: [netlib-scalapack]
        buildable: true
        version: []
        target: ['power9le', 'ppc64le']
        paths: {}
        modules: {}
  ```
  does not concretize specs incapabable of targetting `power9le` as `ppc64le`,
  but does the default behavior described at the top of this issue. Even putting
  the `arch` target in the compiler spec or as a separate vector in an
  environmnent/stack matrix outer-product fails to propogate the requested
  target to specs.

- `spack clean -s` in an environment doesn't seem to actually clear the staging
    directories?

- Lost packages? CMake for XL is installed in 'None':
  ```
  $ spack install -v
  ==> Installing environment test
  ==> cmake@3.16.2 : has external module in cmake
  ==> cmake@3.16.2 : is actually installed in None
  ==> cmake@3.16.2 : already registered in DB
  ==> Installing netlib-lapack
  ==> Searching for binary cache of netlib-lapack
  ==> Finding buildcaches in /sw/sources/spack/mirrors/builds/peak/build_cache
  ==> Fetching file:///sw/sources/spack/mirrors/builds/peak/build_cache/linux-rhel7-power9le-xl-16.1.1-4-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v.spec.yaml
  curl: (37) Couldn't open file /sw/sources/spack/mirrors/builds/peak/build_cache/linux-rhel7-power9le-xl-16.1.1-4-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v.spec.yaml
  ==> Failed to fetch file from URL: file:///sw/sources/spack/mirrors/builds/peak/build_cache/linux-rhel7-power9le-xl-16.1.1-4-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v.spec.yaml
      Curl failed with error 37
  ==> Fetching from file:///sw/sources/spack/mirrors/builds/peak/build_cache/linux-rhel7-power9le-xl-16.1.1-4-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v.spec.yaml failed.
  ==> No binary for netlib-lapack found: installing from source
  ==> Using cached archive: /sw/.testing/belhorn/spack/site-stacks/hosts/peak/var/cache/netlib-lapack/netlib-lapack-3.8.0.tar.gz
  ==> Staging archive: /tmp/belhorn/spack-stage/spack-stage-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/lapack-3.8.0.tar.gz
  ==> Created stage in /tmp/belhorn/spack-stage/spack-stage-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v
  ==> Applied patch /autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/var/spack/repos/builtin/packages/netlib-lapack/ibm-xl.patch
  ==> Applied patch /autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/var/spack/repos/builtin/packages/netlib-lapack/undefined_declarations.patch
  ==> Applied patch /autofs/nccs-svm1_sw/.testing/belhorn/spack/site-stacks/hosts/peak/spack/var/spack/repos/builtin/packages/netlib-lapack/testing.patch
  ==> Ran patch() for netlib-lapack
  ==> Building netlib-lapack [CMakePackage]
  ==> Executing phase: 'cmake'
  ==> [2020-02-04-10:26:41.375818] 'cmake' '/tmp/belhorn/spack-stage/spack-stage-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/spack-src' '-G' 'Unix Makefiles' '-DCMAKE_INSTALL_PREFIX:PATH=/gpfs/alpine/world-shared/stf007/belhorn/spac
  k/stacks/peak/production/opt/linux-rhel7-power9le/xl-16.1.1-4/netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v' '-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo' '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON' '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=FAL
  SE' '-DCMAKE_INSTALL_RPATH:STRING=/gpfs/alpine/world-shared/stf007/belhorn/spack/stacks/peak/production/opt/linux-rhel7-power9le/xl-16.1.1-4/netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/lib;/gpfs/alpine/world-shared/stf007/belhorn/
  spack/stacks/peak/production/opt/linux-rhel7-power9le/xl-16.1.1-4/netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/lib64' '-DCMAKE_PREFIX_PATH:STRING=None' '-DBUILD_SHARED_LIBS:BOOL=OFF' '-DLAPACKE:BOOL=ON' '-DLAPACKE_WITH_TMG:BOOL=ON'
   '-DCBLAS=ON' '-DCMAKE_Fortran_COMPILER=/sw/peak/xl/16.1.1-4/xlf/16.1.1/bin/xlf_r' '-DCMAKE_Fortran_FLAGS= -O3 -qnohot' '-DBUILD_DEPRECATED:BOOL=ON' '-DBUILD_TESTING:BOOL=OFF'
  ==> Error: ProcessError: cmake: No such file or directory: 'cmake'
      Command: 'cmake' '/tmp/belhorn/spack-stage/spack-stage-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/spack-src' '-G' 'Unix Makefiles' '-DCMAKE_INSTALL_PREFIX:PATH=/gpfs/alpine/world-shared/stf007/belhorn/spack/stacks/peak/produc
  tion/opt/linux-rhel7-power9le/xl-16.1.1-4/netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v' '-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo' '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON' '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=FALSE' '-DCMAKE_INSTALL
  _RPATH:STRING=/gpfs/alpine/world-shared/stf007/belhorn/spack/stacks/peak/production/opt/linux-rhel7-power9le/xl-16.1.1-4/netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/lib;/gpfs/alpine/world-shared/stf007/belhorn/spack/stacks/peak/pr
  oduction/opt/linux-rhel7-power9le/xl-16.1.1-4/netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/lib64' '-DCMAKE_PREFIX_PATH:STRING=None' '-DBUILD_SHARED_LIBS:BOOL=OFF' '-DLAPACKE:BOOL=ON' '-DLAPACKE_WITH_TMG:BOOL=ON' '-DCBLAS=ON' '-DCMA
  KE_Fortran_COMPILER=/sw/peak/xl/16.1.1-4/xlf/16.1.1/bin/xlf_r' '-DCMAKE_Fortran_FLAGS= -O3 -qnohot' '-DBUILD_DEPRECATED:BOOL=ON' '-DBUILD_TESTING:BOOL=OFF'
  See build log for details:
    /tmp/belhorn/spack-stage/spack-stage-netlib-lapack-3.8.0-ej4quc7ch3dovus2mkgu7wqxwzyns52v/spack-build-out.txt

  ```
- Autoconf \_make_exectuable does not honor external module-based installs or concretization through externals picks up the incorrect version
  ```
  def _make_executable(self, name):
      return Executable(join_path(self.prefix.bin, name))

  ```
```
$ spack spec -lINt "parallel-io%xl@16.1.1-4"
Input spec
--------------------------------
 -   [    ]  .parallel-io%xl@16.1.1-4

Concretized
--------------------------------
 -   inp6ftz  [    ]  olcf.parallel-io@2.4.4%xl@16.1.1-4 build_type=RelWithDebInfo ~examples arch=linux-rhel7-power9le
 -   laisp5g  [b   ]      ^builtin.cmake@3.16.2%xl@16.1.1-5~doc+ncurses+openssl+ownlibs~qt arch=linux-rhel7-power9le
 -   qryybog  [bl  ]      ^builtin.hdf5@1.10.6%xl@16.1.1-4~cxx~debug+fortran+hl+mpi+pic+shared~szip~threadsafe arch=linux-rhel7-power9le
 -   s2uo2br  [bl  ]          ^builtin.numactl@2.0.12%xl@16.1.1-4 arch=linux-rhel7-power9le
 -   qkkibm2  [b   ]              ^builtin.autoconf@2.69%xl@16.1.1-5 arch=linux-rhel7-power9le
 -   7sy5q7a  [b   ]              ^builtin.automake@1.16.1%xl@16.1.1-5 arch=linux-rhel7-power9le
[+]  b55sxnw  [b   ]              ^builtin.libtool@2.4.2%xl@16.1.1-4 arch=linux-rhel7-power9le
[+]  6djryqh  [b   ]              ^builtin.m4@1.4.18%xl@16.1.1-4 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-rhel7-power9le
[+]  lqvz5ns  [bl  ]                  ^builtin.libsigsegv@2.12%xl@16.1.1-4 arch=linux-rhel7-power9le
[+]  3y2htop  [bl  ]          ^olcf.spectrum-mpi@10.3.0.1-20190611%xl@16.1.1-4 arch=linux-rhel7-power9le
[+]  rsnev7o  [bl  ]          ^builtin.zlib@1.2.11%xl@16.1.1-4+optimize+pic+shared arch=linux-rhel7-power9le
 -   2eob7sc  [bl  ]      ^builtin.netcdf-c@4.7.3%xl@16.1.1-4~dap~hdf4 maxdims=1024 maxvars=8192 +mpi+parallel-netcdf+pic+shared arch=linux-rhel7-power9le
[+]  rjst2ob  [bl  ]          ^builtin.parallel-netcdf@1.12.1%xl@16.1.1-4+cxx+fortran+pic arch=linux-rhel7-power9le
 -   k37xmd4  [bl  ]      ^builtin.netcdf-fortran@4.4.4%xl@16.1.1-4+mpi+pic arch=linux-rhel7-power9le


```
