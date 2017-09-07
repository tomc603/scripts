#!/usr/bin/env bash

if [[ $UID -ne 0 ]]; then
  echo "You must run this utility as root!"
  exit 1
fi

# Restart the mDNSResponder...because it gets confused sometimes
killall -HUP mDNSResponder

# If a directory service is used, this may be helpful to clear
# cached entries causing problems.
# dscacheutil -flushcache
