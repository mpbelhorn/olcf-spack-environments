#!/bin/bash

COMMON_PREFIX="/sw/summit/lmod"
EL7_VER="8.2.10"
EL8_VER="8.4"
VERSION_SYMLINK="${COMMON_PREFIX}/lmod"
DEF_MODPATH="${COMMON_PREFIX}/etc/modulepath.default"


function sync_cache_reminder {
  msg="\nDone. It is now necessary to update the LMOD system cache.\n"
  msg+="Please use a new login as the appropriate user and run\n\n"
  msg+='${LMOD_DIR}/update_lmod_system_cache_files "${MODULEPATH}"'
  msg+="\n\nto finish the swap.\n"
  printf "${msg}"
}


echo "This script will setup the environment module system on Summit for a given RHEL OS release."
echo ""
read -p "Choose RHEL OS version, 8 or 7: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[8]$ ]]; then
  echo "Setting up LMOD for RHEL8"
  unlink "${DEF_MODPATH}" && ln -s modulepath.default.rhel8 "${DEF_MODPATH}"
  unlink "${VERSION_SYMLINK}" && ln -s "${EL8_VER}" "${VERSION_SYMLINK}"
  sync_cache_reminder
elif [[ $REPLY =~ ^[7]$ ]]; then
  echo "Setting up LMOD for RHEL7"
  unlink "${DEF_MODPATH}" && ln -s modulepath.default.rhel7 "${DEF_MODPATH}"
  unlink "${VERSION_SYMLINK}" && ln -s "${EL7_VER}" "${VERSION_SYMLINK}"
  sync_cache_reminder
else
  echo "ERROR: input not understood."
  echo "Please choose '8' or '7'."
fi
