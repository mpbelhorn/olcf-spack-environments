#!/bin/bash

MODULES_PREFIX="/sw/summit/spack-envs/base/modules/spack/linux-rhel8-ppc64le"
SMPI_MODULES_PREFIX="${MODULES_PREFIX}/spectrum-mpi"
SMPI_VERSION="10.4.0.3-20210112"

# echo ""
# echo "==> Possible SMPI modulepaths"
# echo ""
O_IFS=$IFS
POSSIBLE_MPATHS=$(find ${SMPI_MODULES_PREFIX} \
      -mindepth 2 \
      -maxdepth 3 \
      -type d \
      \( -ipath "${SMPI_MODULES_PREFIX}/${SMPI_VERSION}-*/*/*" ! -ipath "*/Core/*" \) \
      -o \( -ipath "*/${SMPI_VERSION}-*/Core" \) \
    | sort -t/ -k11)
IFS=$'\n'
POSSIBLE_MPATHS=($POSSIBLE_MPATHS)
IFS=$O_IFS
# printf '%s\n' "${POSSIBLE_MPATHS[@]}"

# echo ""
# echo "==> Active SMPI modulepaths"
# echo ""
_COMPILERS=$(module --redirect spider "spectrum-mpi/${SMPI_VERSION}" \
            | grep -e "^\s*[a-z]*/[0-9\.a-z\-]*$" \
            | grep -oe "[^ ]*" | sed 's/llvm/clang/g' \
            | sort )
IFS=$'\n'
_COMPILERS=($_COMPILERS)
_COMPILERS+=("Core")
_COMPILERS=($(sort <<<"${_COMPILERS[*]}"))
IFS=$O_IFS
ACTIVE_MPATHS=()
for compiler in ${_COMPILERS[@]}; do
  # /gcc/7.5.0/spectrum-mpi/10.4.0.3-20210112.lua"
  _mpath=$(grep -e "prepend_path.*MODULEPATH" \
          ${MODULES_PREFIX}/${compiler}*/spectrum-mpi/${SMPI_VERSION}.lua \
        | grep -o "$MODULES_PREFIX[^\"\']*")
  ACTIVE_MPATHS+=($_mpath)
done
# printf '%s\n' "${ACTIVE_MPATHS[@]}"

# echo ""
# echo "==> New SMPI modulepaths"
# echo ""
NEW_MPATHS=()
for i in "${POSSIBLE_MPATHS[@]}"; do
    skip=
    for j in "${ACTIVE_MPATHS[@]}"; do
        [[ $i == $j ]] && { skip=1; break; }
    done
    [[ -n $skip ]] || NEW_MPATHS+=("$i")
done
# printf '%s\n' "${NEW_MPATHS[@]}"


# echo ""
# echo "==> Mergeable SMPI modulepaths"
# echo ""
_mask="${SMPI_MODULES_PREFIX}/${SMPI_VERSION}-xxxxxxx/"
for ap in "${ACTIVE_MPATHS[@]}"; do
  target=$(cut -c${#_mask}- - <<< "$ap")
  echo ""
  echo "--> $ap"
  for np in "${NEW_MPATHS[@]}"; do
    if [[ $np =~ $target ]]; then
      echo "  < $np"
      # && echo "The following modulefiles and paths will be updated:" \
      # && echo "+----------- > = sent; < = recieved; c = created; . = not updated; * = message" \
      # && echo "|+---------- (d)irectory; (f)ile; (L)ink; (D)evice; (S)pecial" \
      # && echo "||+--------- (c)hecksum changed" \
      # && echo "|||+-------- (s)ize changed" \
      # && echo "||||+------- (t)imestamp changed" \
      # && echo "|||||+------ (p)permissions changed" \
      # && echo "||||||+----- (o)wner changed" \
      # && echo "|||||||+---- (g)roup changed" \
      # && echo "||||||||+--- N/A" \
      # && echo "|||||||||+-- (a)cl changed" \
      # && echo "||||||||||+- (x)attr changed" \
      # && echo "|||||||||||" \
    xfertmp=$(mktemp) \
      && rsync --dry-run -rlp --ignore-existing --out-format='RSYNC_CONFIRM %i %n%L' \
         "${np}/" \
         "${ap}/" \
         | grep "RSYNC_CONFIRM >" \
         | awk '{ print $3 }' > "${xfertmp}" \
      && rsync --dry-run --ignore-existing  --itemize-changes --files-from=${xfertmp} \
         "${np}/" \
         "${ap}/"
      # echo "Update modulefiles (y/[n])? "
      # read
      # if [[ ${REPLY} = [yY] ]]; then
      #    rsync -v --ignore-existing  --itemize-changes --files-from=${xfertmp} \
      #    "${np}/" \
      #    "${ap}/"
      # fi
      rm -f "${xfertmp}"
    fi
  done
done
