use strict;
use warnings;

my $counter = 0;
my $buffer = 0; # false

my $out = 0;

if ($buffer) {
	print "1 is true\n";
}



sub inv {
	return 0 if ($_[0] == 1);
	return 1;
}

inv("jlkjlk");

foreach (40..78) {
	if ($buffer) {
		$out = inv $buffer; 
		$buffer = !$buffer; 
	} elsif ($counter % 4 == 1 && $counter != 5 && $counter != 9 && $counter != 5+36*4 && $counter != 9+36*4) {
		$out = !$buffer;
		$buffer = !$buffer;  
	}
	$counter++;
	if ($counter>288) {
		$counter=0;
	}
	print "[".$counter."] ".$out."\n";
}