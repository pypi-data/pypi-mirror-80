#!/usr/bin/env bash
# shellcheck disable=SC2034
export source="${BASH_SOURCE[0]}"; debug.sh source

if ! isuser.sh; then
  error.sh "can not be done with root"; exit 1
fi

if name="$( source gtop 2>&1 )"; then
  export name; debug.sh name
  path="$( git rev-parse --show-toplevel 2>&1 )"; export path; debug.sh path
  cd "${path}" || { error.sh cd "${path}"; exit 1; }
  if error="$( git add . --all 2>&1 )"; then
    info.sh add "${name}"; exit 0
  else
    error.sh add "${name}" "${error}"; exit 1
  fi
  cd - > /dev/null || exit 1
else
  error.sh gall "${name}"; exit 1
fi

unset source name path error
