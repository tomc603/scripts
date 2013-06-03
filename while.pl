#!/usr/bin/perl

use Error qw(:try);

my $MAXTRIES = 3;

my $retries = 0;
my $last = 0;
while ($retries++ < $MAXTRIES) {
	try {
		my $intry = 1;
		throw Error("Generic error!");
	} otherwise {
		print "An unexpected exception was encountered! Quitting.\n";
		$last = 1;
	};
	last if $last;
}

# See if we can access vars created in a previous try/catch
try {
	print "Intry is $intry\n";
} otherwise {
	print "Trying to print intry failed!\n";
};

print "Done $retries tries.\n";
