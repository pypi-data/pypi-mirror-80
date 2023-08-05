#!/usr/bin/env bash
# shellcheck disable=SC2034
export source="${BASH_SOURCE[0]}"; debug.sh source

if ! isuser.sh; then
  error.sh "can not be done with root"; exit 1
fi

case "${1}" in
  major) bump="${1}" ;;
  minor) bump="${1}" ;;
  patch) bump="${1}" ;;
esac; shift

test -n "${PROJECT_BASHRC}" || { error.sh "PROJECT_BASHRC" "empty"; exit 1; }
cd "${PROJECT_BASHRC}" > /dev/null 2>&1 || { error.sh "${PROJECT_BASHRC}" "does not exists"; exit 1; }

project-upload.sh "${PROJECT_BASHRC}" "${bump}" "${GITHUB_USERNAME}" || exit 1

cd - > /dev/null || exit 1

unset source bump
