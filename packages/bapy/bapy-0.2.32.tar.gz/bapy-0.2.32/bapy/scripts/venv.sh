#!/usr/bin/env bash
# shellcheck disable=SC1090
# shellcheck disable=SC2034
# ${1} - path
# ${2} - bump: <major|minor>
# ${3} - twine: <"${GITHUB_USERNAME}"|"${GITHUB_ORGANIZATION_ID}"|pypi>
export starting="${BASH_SOURCE[0]}"; debug.sh starting

if ! isuserdarwin.sh && [[ "${USERNAME}" == "${USER}" ]]; then
  error.sh "can not be done with root"; exit 1
fi

if [[ "${1-}" ]]; then
  while (( "$#" )); do
    case "${1}" in
      bapy) name="${1}"; path="${BAPY}" ;;
      pen) name="${1}"; path="${PEN}" ;;
      site) site="${1}" ;;
      *) path="${PEN}"; name="$( basename "${path}" )" ;;
    esac; shift
  done
else
  path="${BAPY}"; name="$( basename "${path}" )"
fi

export BAPY PEN path name; debug.sh BAPY PEN path name

cd "${path}" > /dev/null 2>&1 || { error.sh "${path}" "invalid"; exit 1; }

virtual="${path}/venv/bin/"
export virtual; debug.sh virtual

if isuser.sh; then
  # shellcheck disable=SC2154
  #  export site in project-upload.sh (default use virtual environment if no defined)
  if test -z "${site}"; then
    if ! test -d "${virtual}"; then
      if error="$( python3.8 -m venv "${path}/venv" 2>&1 )"; then
        info.sh venv "${name}"
      else
        error.sh venv "${name}" "${error}"; exit 1
      fi
    fi
    source "${virtual}/activate"
  else
    warning.sh venv "${name}" site
  fi
  while read -r file; do
    export file; debug.sh file
    if error="$( "${virtual}python3" -m pip install --upgrade pip wheel setuptools && \
                 "${virtual}python3" -m pip install --upgrade -r "${file}" 2>&1 )"; then
      info.sh requirements "${name}" "${file}"
    else
      error.sh requirements "${name} ${file}" "${error}"; exit 1
    fi
  done < <( find "${path}" -mindepth 1 -maxdepth 2 -type f -name "requirements*" )
else
  error.sh "${BASHRC}" "can not be uploaded with root"; exit 1
fi

cd - > /dev/null || exit 1

unset starting virtual file error name path site
