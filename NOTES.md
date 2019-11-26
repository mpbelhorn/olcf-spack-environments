
# Build Problems

## Peak

- raja@0.5.3%gcc@8.1.1 on peak: `__ieee128` C++ error.
- papi: filter_file over `**/*.[ch]` hangs on random files.
- `netcdf-fortran%xl`: libtool calls do not include `-L` arguments for
    `Spec('netcdf)['hdf5']` libraries despite those paths being in
    `SPACK_LINK_DIRS` and `SPACK_RPATH_DIRS`
  - Solution(?): enforce hdf5 dependency when building with xl?

# Maintenance problems

- Unregistering packages from spack DB in an environment?
- Uninstalling package from env without removing it from env SpecList
  - No way to current remove specs expanded from a matrix, but sometimes there
    is a need to be rebuild such packages (along with their dependents).
  - Often want to remove modules for such packages as well, especially if module
      is initially for an "external" build.
  - Generally do not wish to change the spec list, just remove the old builds
      and modules.

- Cannot `spack find` one-off specs, notably built with CLI cflags and fflags
    arguments.
  - `spec -lINt` shows them as installed, but `find` with either a hash argument
      or partial spec fails to find them.

- `blacklist_implicits: True` fails to publish any modulefiles for LMOD.
