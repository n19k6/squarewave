use strict;
use warnings;


# perl -e "print ((2**8-1)*64/1000)"


my %wanted;



%wanted = ();
$wanted{1} = 0.1; # 001->-0.933->0.117

my %start;
my %multi;

#foreach my $TCNT2 (0..254) {
#foreach my $TCNT2 (0..200) {
#	my $tick = (255-$TCNT2)*64/1000; #ms
#	my $period = $tick*20/1000; #s
#	my $f = 1/$period; #Hz
#	print sprintf("%03d",$TCNT2)."->".sprintf("%8.3f",$f).sprintf("%8.3f",$f/2).sprintf("%8.3f",$f/3).sprintf("%8.3f",$f/4).sprintf("%8.3f",$f/5).sprintf("%8.3f",$f/6).sprintf("%8.3f",$f/7).sprintf("%8.3f",$f/8).sprintf("%8.3f",$f/9).sprintf("%8.3f",$f/10)."\n";
#}





#foreach my $key (sort {$a <=> $b} keys %wanted) {
#	#print "[".$key."-".$wanted{$key}."] = [".dump_opt($wanted{$key})."]\n";
#	#print $key.",";
#	print $start{$key}.",";
#}
#print "\n";

=for
1010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010
1010101010101010101010101010101010101010101010101010101010101010101000001010101010101010101010101010101010101010101010101010101010101010101000
=cut

foreach my $key (0..143) {
	if ($key % 2 == 0 and $key != 68 and $key != 70 and $key != 68+72 and $key != 70+72) {
		print "1,";
	} else {
		print "0,";
	}
}
print "\n";

foreach my $key (0..143) {
	if ($key == 2 or $key == 2+36 or $key == 2+2*36 or $key == 2+3*36) {
		print "0,";
	} else {
		print "1,";
	}
}
print "\n";

foreach my $key (0..143) {
	if ($key == 3 or $key == 4 or $key == 3+36 or $key == 4+36 or $key == 3+3*36 or $key == 4+3*36) {
		print "1,";
	} else {
		print "0,";
	}
}
print "\n";