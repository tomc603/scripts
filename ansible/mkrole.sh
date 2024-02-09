#!/usr/bin/env bash

# This script creates a new Ansible role by creating a playbook and the base
# directory structure described in the Ansible documentation.

ROLENAME=$1
ROLEDIR="roles/${ROLENAME}"
ROLESUBDIRS="defaults files handlers meta tasks templates vars"

function yml_header() {
  echo -e "---\n# Copyright YYYY Author\n"
}

if [[ -z ${ROLENAME} ]]; then
  echo "You must specify a role name"
  exit 1
fi

# Create an empty role file
yml_header > ${ROLENAME}.yml

# Create an empty role directory structure
for d in $ROLESUBDIRS; do
  mkdir -p ${ROLEDIR}/${d}
done
