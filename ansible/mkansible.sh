#!/usr/bin/env bash

# This script creates a new Ansible directory structure by creating the basic
# directory structure described in the Ansible documentation.

ANSIBLENAME=$1
ANSIBLEDIRS="filter_plugins group_vars host_vars library roles"

if [[ -z ${ANSIBLENAME } ]]; then
  echo "You must specify a directory name"
  exit 1
fi

# Create an empty directory structure
for d in $ANSIBLEDIRS; do
  mkdir -p ${ANSIBLENAME}/${d}
done

# Create an empty config file
touch ${ANSIBLENAME}/ansible.cfg
