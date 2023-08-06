#!/usr/bin/env bash

if [[ "$( hostname )" == "kali" ]]; then
  if  [[ "$(id -u)" != "0" ]]; then
    exit
  else
    exit 1
  fi
else
  if [[ "$(id -u)" != "0" ]] && [[ ! "${SUDO_UID-}" ]]; then
    exit
  else
    exit 1
  fi
fi
