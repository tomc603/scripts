#!/usr/bin/env bash

#
# Install GRUB bootloader
#

set -e

sudo grub-install -v --no-floppy --removable \
    --boot-directory /mnt/usb/boot \
    --efi-directory=/mnt/usb/boot/efi \
    --target=x86_64-efi /dev/sda
