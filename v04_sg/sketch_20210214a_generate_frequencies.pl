use strict;
use warnings;


# perl -e "print ((2**8-1)*64/1000)"

# poti: values from 0-31, 0=off, 31=on, 30 ~10 Hz

# frequency, period -> https://circuitglobe.com/difference-between-period-and-frequency.html

# bei 10 Hz soll ein signal 0,1s = 100ms dauern
# bei einer unterteilung von 20 teilen (0%, 5%, 10%, ..) fuer den dutycycle muss 10ms getriggert werden

# 16.384 ms (2**8*64/1000 = 16.384)
# timer2 trigger aktuell mit prescale 1024 zwischen folgenden zweiten
# 0=16.384
# 254=16.384/255,256?
# 255= not defined
# ergebnis: timer ist nicht langsam genug um 10/3 Hz ~ 0.3 Hz abzubilden

# welche tick-frequenz wird aktuell bei einem prescale von 1024 abgebildet
# welcher signal-frequenz entspricht dies
# durchmessen!

# fuer jede frequenz+duty cycle die Werte TCNT2, overflow und 1->0 counter berechnen

# 0   1    2    3    4    5     6
# 0.1
# mapping 10 logarithmisch
# [-1..1] -> 10**x, i.e.
# 10**-1 = 0.1 Hz
# 10**0 = 1 Hz
# 10**1 = 10 Hz

#foreach my $i (1..30) {
#	my $v = ($i-15)/15;
#	print '$wanted{'.$i.'} = '.sprintf("%.3f",10**$v).'; # '.sprintf("%03d",$i)."->".sprintf("%.3f",$v)."->".sprintf("%.3f",10**$v)."\n";
#}
#print "\n\n";
#exit 0;

my %wanted;

$wanted{1} = 0.1; # 001->-0.933->0.117
$wanted{2} = 0.13; # 002->-0.867->0.136
$wanted{3} = 0.15; # 003->-0.800->0.158
$wanted{4} = 0.18; # 004->-0.733->0.185
$wanted{5} = 0.2; # 005->-0.667->0.215
$wanted{6} = 0.25; # 006->-0.600->0.251
$wanted{7} = 0.3; # 007->-0.533->0.293
$wanted{8} = 0.35; # 008->-0.467->0.341
$wanted{9} = 0.4; # 009->-0.400->0.398
$wanted{10} = 0.45; # 010->-0.333->0.464
$wanted{11} = 0.55; # 011->-0.267->0.541
$wanted{12} = 0.6; # 012->-0.200->0.631
$wanted{13} = 0.8; # 013->-0.133->0.736
$wanted{14} = 0.9; # 014->-0.067->0.858
$wanted{15} = 1.000; # 015->0.000->1.000
$wanted{16} = 1.2; # 016->0.067->1.166
$wanted{17} = 1.4; # 017->0.133->1.359
$wanted{18} = 1.6; # 018->0.200->1.585
$wanted{19} = 1.8; # 019->0.267->1.848
$wanted{20} = 2.2; # 020->0.333->2.154
$wanted{21} = 2.5; # 021->0.400->2.512
$wanted{22} = 2.9; # 022->0.467->2.929
$wanted{23} = 3.4; # 023->0.533->3.415
$wanted{24} = 4; # 024->0.600->3.981
$wanted{25} = 4.6; # 025->0.667->4.642
$wanted{26} = 5.4; # 026->0.733->5.412
$wanted{27} = 6.3; # 027->0.800->6.310
$wanted{28} = 7.4; # 028->0.867->7.356
$wanted{29} = 8.6; # 029->0.933->8.577
$wanted{30} = 10; # 030->1.000->10.000

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



#my $abstand=100;
#foreach my $multiplier (1..16) {
#foreach my $TCNT2 (0..200) {
#	my $tick = (255-$TCNT2)*64/1000; #ms
#	my $period = $tick*20/1000; #s
#	my $f = 1/$period; #Hz
#	#print sprintf("%03d",$TCNT2)."->".sprintf("%8.3f",$f).sprintf("%8.3f",$f/2).sprintf("%8.3f",$f/3).sprintf("%8.3f",$f/4).sprintf("%8.3f",$f/5).sprintf("%8.3f",$f/6).sprintf("%8.3f",$f/7).sprintf("%8.3f",$f/8).sprintf("%8.3f",$f/9).sprintf("%8.3f",$f/10)."\n";
#	if (abs($f/$multiplier - 1.234) < $abstand) {
#		$abstand = abs($f/$multiplier - 1.234);
#		print sprintf("%03d",$TCNT2).", ".sprintf("%03d",$multiplier)."->".sprintf("%8.3f",$f/$multiplier).sprintf("%8.3f",$abstand)."\n";
#	}
#}
#}

foreach my $key (sort {$a <=> $b} keys %wanted) {
	print "\/\/[".$key."-".$wanted{$key}."] = [".dump_opt($wanted{$key}, $key)."]\n";
}


foreach my $key (sort {$a <=> $b} keys %wanted) {
	#print "[".$key."-".$wanted{$key}."] = [".dump_opt($wanted{$key})."]\n";
	#print $key.",";
	print $start{$key}.",";
}
print "\n";

foreach my $key (sort {$a <=> $b} keys %wanted) {
	#print "[".$key."-".$wanted{$key}."] = [".dump_opt($wanted{$key})."]\n";
	#print $key.",";
	print $multi{$key}.",";
}
print "\n";

foreach my $key (sort {$a <=> $b} keys %wanted) {
	#print "[".$key."-".$wanted{$key}."] = [".dump_opt($wanted{$key})."]\n";
	print sprintf("%8.2f",(255-$start{$key})*64/1000).",";
}
print "\n";

foreach my $key (sort {$a <=> $b} keys %wanted) {
	#print "[".$key."-".$wanted{$key}."] = [".dump_opt($wanted{$key})."]\n";
	print sprintf("%8.2f",1/((255-$start{$key})*64/1000*20/1000*$multi{$key})).",";
}
print "\n";


=for comment
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
=cut

print "test\n";


sub dump_opt {
	
	my ($val,$i) = @_;
	my ($m, $tcnt,$fq) = (0,0,0);
	
	my $abstand=100;
	foreach my $multiplier (1..64) {
		foreach my $TCNT2 (0..200) {
			my $tick = (255-$TCNT2)*64/1000; #ms
			my $period = $tick*20/1000; #s
			my $f = 1/$period; #Hz
			#print sprintf("%03d",$TCNT2)."->".sprintf("%8.3f",$f).sprintf("%8.3f",$f/2).sprintf("%8.3f",$f/3).sprintf("%8.3f",$f/4).sprintf("%8.3f",$f/5).sprintf("%8.3f",$f/6).sprintf("%8.3f",$f/7).sprintf("%8.3f",$f/8).sprintf("%8.3f",$f/9).sprintf("%8.3f",$f/10)."\n";
			if (abs($f/$multiplier - $val) < $abstand) {
				$abstand = abs($f/$multiplier - $val);
				$m = $multiplier;
				$tcnt = $TCNT2;
				#print sprintf("%03d",$TCNT2).", ".sprintf("%03d",$multiplier)."->".sprintf("%8.3f",$f/$multiplier).sprintf("%8.3f",$abstand)."\n";
			}
		}
	}
	$fq = 1/((255-$tcnt)*64/1000*20/1000);
	$fq = $fq/$m;
	#print $val."\n";
	$start{$i} = $tcnt;
	$multi{$i} = $m;
	return sprintf("%03d",$tcnt).", ".sprintf("%03d",$m)."->".sprintf("%8.3f",$fq).sprintf("%8.3f",$abstand);
}
