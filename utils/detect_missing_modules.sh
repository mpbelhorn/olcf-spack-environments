#!/bin/bash
#
# A utility to find and refresh modulefiles for explicitly installed packages
# that are missing a modulefile. Modulefiles for installed packages may be
# missing if, while installing specs from a spack environment file, one or more
# build failures prevented spack from generating modulefiles for any
# new and successfully installed specs during the run.
#
# This script allows refreshing modules only for explicitly-installed packages
# which did not get a modulefile generated at install time while preserving any
# and all existing modulefiles. Ie, this allows for spack to generate missing
# modulefiles without refreshing all existing modulefiles and mimics the
# behavior of classic spack v<0.16 when generating or preserving an existing
# modulefile that conflicts with a module that would be generated for a new
# build. The intent is to minimize changes to packages/builds that are in
# production which might be currently employed by users' jobs.

# TODO: ensure spack env is setup and this script is executed by sourcing it in
# a shell with the target spack environment activated.

# FIXME: Get from user input the date after which any installed explicit
# packages missing modulefiles should have modules refreshed.
DATE_START="2021-12-15"

# FIXME: Uniqify this tmp file
TMP_FILE="/tmp/$USER/new_packages.log"
mkdir -p "/tmp/$USER"

# Find all packages explicitly installed since a given date and store in a tmp
# file.
if [ ! -f "${TMP_FILE}" ]; then
  spack find \
    -lxv \
    --show-full-compiler \
    --no-groups \
    --start-date "${DATE_START}" > "${TMP_FILE}"
fi

# Extract unique hash for each package in spack CLI spec-by-hash format.
SPECS="$(grep -v -e "----" -e "==" -e "^$" "${TMP_FILE}" \
  | awk '{ print $1 }' \
  | sed -e 's|^\(.*\)$|/\1|')"

# Collect all package hashes for installations that do not have a modulefile
# FIXME: find a way to speed up this operation. This would be faster if this
# script were a spack command extension written in Python and using spack's
# python API.
REFRESH_LIST=""
while IFS= read -r spec; do
  # spack module lmod find --full-path "$(tr -d '\n' <<< $spec)"
  MODPATH="$(spack module lmod find --full-path "${spec}" 2>/dev/null)"
  if [ $? = 1 ]; then
    echo "Spec '${spec}' : No modulefile found"
    REFRESH_LIST+=" ${spec}"
    # break
  elif [ -f "${MODPATH}" ]; then
    echo "Spec '${spec}' : '${MODPATH}'"
  else
    echo "Spec '${spec}' : No modulefile found"
    REFRESH_LIST+=" ${spec}"
  fi
done <<< "$SPECS"

# Trim excess whitespace from the list of specs needing modulefiles.
REFRESH_LIST="${REFRESH_LIST## }"
echo ""
echo "Found the following specs missing modulefiles:"
echo "${REFRESH_LIST}"
echo ""

# Refresh the modulefiles
if [ ${#REFRESH_LIST} -gt 0 ]; then
  spack module lmod refresh ${REFRESH_LIST}
fi

# Clean up tmp file.
rm "${TMP_FILE}"
