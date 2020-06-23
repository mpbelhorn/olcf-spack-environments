# OLCF Spack Environments

This repo contains the infrastructure and environment definitions to deploy
site-provided software on OLCF resources via Spack environments.

## Getting Started

Clone this repo and it's facility-modified spack fork somewhere on an OLCF
filesystem:

```
git clone --recurse-submodules gitlab@gitlab.ccs.ornl.gov:belhorn/facility-spack-environments.git
```

or

```
git clone --recurse-submodules https://gitlab.ccs.ornl.gov/belhorn/facility-spack-environments.git
```

Next, modify the init script and environment on a new branch to point to
locations where you can write.

In `./init-peak.sh`, update `export ENV_PREFIX="${ENV_PREFIX:-/sw/.b2/envs}"`
with a default `ENV_PREFIX` path under which you wish to install the
environments tracked in this repo. From this variable, a unique path per system
and environment name will be constructed:

```
ENV_ROOT="${ENV_PREFIX}/${_THIS_HOST}/${ENV_NAME}"
```

By default, `ENV_NAME="base"` unless the variable `ENV_NAME` already exists in
the environment and an associated environment with that name for the current
host system is tracked in this repo. The value of `${_THIS_HOST}` is determined
automatically from the hostname on which the init script is being run. For each
system and environment tracked in this repo that you wish to work on, ensure
that the `ENV_ROOT` directory exists and has the following subdirectories, each
owned by your username:

```
${ENV_ROOT}/opt
${ENV_ROOT}/modules/lmod
${ENV_ROOT}/modules/tmod
```

The variable `${ENV_ROOT}` is exported in Spack's runtime environment and is
referred to in the `spack.yaml` the enviornment files tracked in this repo to
establish portable and relocatable spack environments using a single set of
configuration files.

The rest of the configuration in the `spack.yaml` environments is expressed
in terms of relative paths to the spack instance used by this repo with a couple
exceptions:

- Mirrors
- Extensions

Spack does not internally expand environment variables in the configuration of
these items so they must be expressed as hard-coded full path strings. The
default values in this repo should point to permanent world-readable paths on
the OLCF filesystem populated with OLCF-maintained extensions and mirrors.

## Spack Fork

The upstream development branch of spack is not used directly. Instead, the OLCF
has implemented some customizations that are tracked in the "olcf-X.Y.Z"
branches of a [facility fork of spack](https://gitlab.ccs.ornl.gov/belhorn/facility-spack)
where `X.Y.Z` refers to the tagged release of upstream spack from which the
OLCF-modified branch is forked.
