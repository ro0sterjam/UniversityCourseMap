use strict;
use warnings;
package Util;

sub trim {
	my ($class, $string) = @_;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}

1;