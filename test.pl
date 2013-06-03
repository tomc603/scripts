#!/usr/bin/perl

use strict;
use warnings;

if (system() > 0) { die "Could not copy file: $!" };
printf("We didn't die! Consider this success!\n");
