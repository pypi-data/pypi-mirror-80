#!/usr/bin/env bash
# ${1} - path
# ${2} - bump: <major|minor>
# ${3} - twine: <"${GITHUB_USERNAME}"|"${GITHUB_ORGANIZATION_ID}"|pypi>
# shellcheck disable=SC2034
export source="${BASH_SOURCE[0]}"; debug.sh source

if ! isuser.sh; then
  error.sh "can not be done with root"; exit 1
fi

path="${1:-.}"

cd "${path}" > /dev/null 2>&1 || { error.sh "${path}" "invalid"; exit 1; }

path="$( pwd )"
name="$( basename "${path}" )"
export path name; debug.sh path name

virtual="${path}/venv/bin"
export virtual; debug.sh virtual

if isuser.sh; then
  if ! test -d "${virtual}"; then
    if error="$( python3.8 -m venv "${path}/venv" 2>&1 )"; then
      info.sh venv "${name}"
    else
      error.sh venv "${name}" "${error}"; exit 1
    fi
  fi
  # shellcheck disable=SC1090
  source "${virtual}/activate"
  while read -r file; do
    export file; debug.sh file
    if error="$( "${virtual}/python3" -m pip install --upgrade pip wheel setuptools && \
                 "${virtual}/python3" -m pip install --upgrade -r "${file}" 2>&1 )"; then
      info.sh requirements "${name}" "${file}"
    else
      error.sh requirements "${name} ${file}" "${error}"; exit 1
    fi
  done < <( find "${path}" -mindepth 1 -maxdepth 2 -type f -name "requirements*" )
else
  error.sh "${PROJECT_BASHRC}" "can not be uploaded with root"; exit 1
fi

cd - > /dev/null || exit 1

unset source virtual file error name path
