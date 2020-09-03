# OLCF Spack Environments

This repo contains the infrastructure and environment definitions to deploy
site-provided software on OLCF resources via Spack environments.

## Getting Started

Clone this repo and it's facility-modified spack fork somewhere on an OLCF
filesystem:

```
git clone --recurse-submodules git@github.com:mpbelhorn/olcf-spack-environments.git
```

or

```
git clone --recurse-submodules https://github.com/mpbelhorn/olcf-spack-environments
```

Next, initialize spack and the build environment. This is done by calling

```
FACSPACK_MY_ENVS=/path/to/host-specific/private/envs FACSPACK_ENV_NAME=base . ./init-facility-spack.sh
```

This will configure the spack build- and run-time environment build and install
the facility spack environment `FACSPACK_ENV_NAME` tracked by this repo for the
current machine in a private location under `FACSPACK_MY_ENVS`. Both of these
variables are optional. If omitted, each variable will take on their default
values:

```
FACSPACK_MY_ENVS="/sw/${_THIS_HOST}/spack-envs"
FACSPACK_ENV_NAME="base"
```

such that sourcing this script by itself

```
. ./init-facility-spack.sh
```

will setup the runtime shell environment to manipulate the production spack
environment on the current system.

This repo will always track at least one spack environment per machine named
`base` which is the complete standard software environment used in production
for that machine. Furthermore, only the user account with owner permissions on
the production environment may be used to manipulate it in the default
`FACSPACK_MY_ENVS`.  This is an intentional safety mechanism to prevent multiple
users from concurrently modifying the production environment. Users may set an
alternate `FACSPACK_MY_ENVS` under which they can run build tests using any
tracked `hosts/${_THIS_HOST}/${FACSPACK_ENV_NAME}/spack.yaml` file in this repo.

From these variables, a unique path per each environment name will be
constructed:

```
FACSPACK_ENV="${FACSPACK_MY_ENVS}/${FACSPACK_ENV_NAME}"
```

The value of `${_THIS_HOST}` is determined automatically from the hostname on
which the init script is being run. For each system and environment tracked in
this repo that you wish to work on, ensure that the final expanded value of
`FACSPACK_ENV` corresponds to an actual existing directory.

Configuration paths in our `spack.yaml` environments that are not fixed to
universal values are expressed in terms of relative paths to either the spack
instance setup by `init-facility-spack` or the path to the `FACSPACK_MY_ENVS`.
These paths are referenced in the `spack.yaml` files via environment variables
set by `init-facility-spack`. This allows the `spack.yaml` environment files to
define portable and relocatable spack environments which can be re-deployed in
arbitrary private locations by any users without needing to modify the
environment file.

The following variables are exported in Spack's runtime environment by
`init-facility-spack` and can be referred to in the `spack.yaml` the enviornment
files tracked in this repo. 

- `${FACSPACK_ENV}`:
      Path to where spack environment will be installed. Contains subdirs `opt`
      and `modules`.
- `${FACSPACK_ENV_MODULEROOT}`:
      Shortcut to `${FACSPACK_ENV}/modules` under which static and
      spack-generated modules are generated. Contains subdirectories `spack`,
      `flat`, and `site` corresponding to lmod, tcl, and static modulefiles
      respectively.
- `${FACSPACK_CONF_COMMON}`:
      Path to facility-wide common configuration files under `${this_repo}/share`.
- `${FACSPACK_CONF_HOST}`:
      Path to host-specific configuration files under `${this_repo}/hosts/${_THIS_HOST}`

There are (as of spack v0.15.0) a couple exceptional paths used in `spack.yaml`
files which cannot de-reference environment variables. These affect

- Mirrors
- Extensions

Spack does not internally expand environment variables in the configuration of
these items so they must be expressed as hard-coded full path strings. The
default values in this repo should point to permanent world-readable paths on
the OLCF filesystem populated with OLCF-maintained extensions and mirrors.

## Spack Fork

The upstream development branch of spack is not used directly. Instead, the OLCF
has implemented some customizations that are tracked in the "olcf-X.Y.Z"
branches of a [facility fork of spack](https://github.com/mpbelhorn/olcf-spack/tree/olcf-0.15.0)
where `X.Y.Z` refers to the tagged release of upstream spack from which the
OLCF-modified branch is forked.
