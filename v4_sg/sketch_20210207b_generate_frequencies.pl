use strict;
use warnings;

# poti: values from 0-127, 0=off, 127=on, 126=10 Hz

foreach my $poti (1..63) {
	my $frequency;
	my $t;
	$frequency = 10/63*$poti;
	$t = 1.0/$frequency;
	my $b;
	if ($frequency<10) {
		$b=" ";
	} else {
		$b="";
	}
	print sprintf("%03d",$poti)."-$b".sprintf("%.3f",$frequency)." Hz-".sprintf("%.3f",$t)." T";#."\n";
	print "   [".sprintf("%.3f",$t*1000/20)."-".sprintf("%.3f",($t*1000/20)*1000/256)."]\n";
}
