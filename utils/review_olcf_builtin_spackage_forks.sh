#!/bin/bash

#####################
# Obtain the path to this file.
#   `_THIS`  : path to this file
#   `TOP_DIR`: path to parent directory of ${_THIS}
# First determine if script is sourced or executed
if [[ "$0" != "${BASH_SOURCE:-}" ]]; then
  # Script is sourced
  _SOURCED=1
  if [ -z "${BASH_SOURCE:-}" ]; then
    _THIS="$(which $0)"
  else
    _THIS="${BASH_SOURCE[0]}"
  fi
else
  # Script is executed
  _SOURCED=0
  _THIS="${BASH_SOURCE[0]}"
fi
while [ -h "$_THIS" ]; do
  # resolve $_THIS until the file is no longer a symlink
  TOP_DIR="$( cd -P "$( dirname "$_THIS" )" >/dev/null && pwd )"

  # if $_THIS was a relative symlink, we need to resolve it relative to the
  # path where the symlink file was located
  _THIS="$(readlink "$_THIS")"
  [[ $_THIS != /* ]] && _THIS="$TOP_DIR/$_THIS" 
done
TOP_DIR="$( cd -P "$( dirname "$_THIS" )" >/dev/null && pwd )"
#####################

repo_root="$(dirname ${TOP_DIR})"
olcf_repo="$repo_root/share/spack/repos/olcf/packages"
builtin_repo="$repo_root/spack/var/spack/repos/builtin/packages"

# Directories in the OLCF repo.
ls -1 $olcf_repo \
  | sort > olcf.pkg_dirs.log

# Directories in the OLCF repo that are actual spackages.
rm  -f olcf.pkgs.log
while read dir; do
  [ -f "$olcf_repo/$dir/package.py" ] && echo "$dir" >> olcf.pkgs.log
done < olcf.pkg_dirs.log

# Directories in the OLCF repo that no longer have a package.py
comm -3 olcf.pkgs.log olcf.pkg_dirs.log > olcf.empty_dirs.log

# Find OLCF packages that are not in the builtin repo.
rm -f olcf.no_upstream.pkgs.log olcf.upstream_pkgs.log olcf.empty_upstream_pkgs.log
while read pkg; do
    if [ ! -d "$builtin_repo/$pkg" ]; then
      echo "$pkg" >> olcf.no_upstream_pkgs.log
    elif [ -f "$builtin_repo/$pkg/package.py" ]; then
      echo "$pkg" >> olcf.upstream_pkgs.log
    else
      echo "$pkg" >> olcf.empty_upstream_pkgs.log
    fi
done < olcf.pkgs.log

readarray -t pkgs < olcf.upstream_pkgs.log
# mapfile -t pkgs < olcf.upstream_pkgs.log
for pkg in "${pkgs[@]}"; do
  read -p "Inspect '$pkg' diff? ([y]/n/q) " -n 1 -r
  echo
  case $REPLY in
     [Nn]*)
       echo "Skipping diff review for '$pkg'"
       continue
       ;;
     [Qq]*)
       echo "Quitting: skipping remaining packages"
       break
       ;;
     [Yy]*)
       ;&
     *)
       vimdiff "$olcf_repo/$pkg/package.py" "$builtin_repo/$pkg/package.py"
       ;;
  esac  
done

## Alternate loop over packages occupying stdin
# while read pkg; do
#   read -p "Inspect '$pkg' diff? ([y]/n/a) " -u 3 -n 1 -r
#   echo
#   case $REPLY in
#      ^[Nn]*)
#        echo "Skipping diff review for '$pkg'"
#        continue
#        ;;
#      ^[Aa]*)
#        echo "Aborting!"
#        break
#        ;;
#      ^[Yy]*)
#        ;&
#      *)
#        vimdiff "$olcf_repo/$pkg/package.py" "$builtin_repo/$pkg/package.py"
#        ;;
#   esac  
# done 3<&0 <olcf.upstream_pkgs.log
