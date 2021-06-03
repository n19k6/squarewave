use strict;
use warnings;
use Math::Trig;

#print "hello\n";

# this script generates a gear with 34 tooths and 2 gaps
# parameters are: radius and tooths hight

#print sin(pi()/2);
my $cx = 100;
my $cy = 100;

my $sr = 50;
my $br = 55;

my @scx; # small circle x-component
my @scy; # small circle y-component
my @bcx; # big circle x-component
my @bcy; # big circle x-component

foreach my $i (0..143) {
	$scx[$i] = $cx+$sr*sin(2*pi()/144*($i-0.5));
	$scy[$i] = $cy-$sr*cos(2*pi()/144*($i-0.5));
	$bcx[$i] = $cx+$br*sin(2*pi()/144*($i-0.5));
	$bcy[$i] = $cy-$br*cos(2*pi()/144*($i-0.5));
}

#print<<EOT
#<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
#EOT

print '<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">'."\n";

# foreach my $i (0..143) {
	# print '<circle cx="'.sprintf("%.3f", $scx[$i]).'" cy="'.sprintf("%.3f", $scy[$i]).'" r="1" stroke="red" fill="transparent" stroke-width="1"/>'."\n";
	# print '<circle cx="'.sprintf("%.3f", $bcx[$i]).'" cy="'.sprintf("%.3f", $bcy[$i]).'" r="1" stroke="blue" fill="transparent" stroke-width="1"/>'."\n";
# }

print '<path d="M '.sprintf("%.3f", $scx[0]).' '.sprintf("%.3f", $scy[0]).' ';
foreach my $i (0..33) {
	print 'L '.sprintf("%.3f", $bcx[$i*4]).' '.sprintf("%.3f", $bcy[$i*4]).' ';
	#print 'L '.sprintf("%.3f", $bcx[$i*4+1]).' '.sprintf("%.3f", $bcy[$i*4+1]).' ';
	print 'A '.sprintf("%.3f", $br).' '.sprintf("%.3f", $br).' 0 0 1 '.sprintf("%.3f", $bcx[$i*4+1]).' '.sprintf("%.3f", $bcy[$i*4+1]).' ';
	print 'L '.sprintf("%.3f", $scx[$i*4+1]).' '.sprintf("%.3f", $scy[$i*4+1]).' ';
	#print 'L '.sprintf("%.3f", $scx[$i*4+4]).' '.sprintf("%.3f", $scy[$i*4+4]).' ';
	print 'A '.sprintf("%.3f", $sr).' '.sprintf("%.3f", $sr).' 0 0 1 '.sprintf("%.3f", $scx[$i*4+4]).' '.sprintf("%.3f", $scy[$i*4+4]).' ';
}
print 'A '.sprintf("%.3f", $sr).' '.sprintf("%.3f", $sr).' 0 0 1 '.sprintf("%.3f", $scx[0]).' '.sprintf("%.3f", $scy[0]).' ';
print 'Z" stroke="green" fill="transparent"/>'."\n";


print '<path transform="translate(120)" d="M '.sprintf("%.3f", $scx[0]).' '.sprintf("%.3f", $scy[0]).' ';
foreach my $i (0..3) {
	print 'L '.sprintf("%.3f", $bcx[$i*36]).' '.sprintf("%.3f", $bcy[$i*36]).' ';
	#print 'L '.sprintf("%.3f", $bcx[$i*4+1]).' '.sprintf("%.3f", $bcy[$i*4+1]).' ';
	print 'A '.sprintf("%.3f", $br).' '.sprintf("%.3f", $br).' 0 0 1 '.sprintf("%.3f", $bcx[$i*36+1]).' '.sprintf("%.3f", $bcy[$i*36+1]).' ';
	print 'L '.sprintf("%.3f", $scx[$i*36+1]).' '.sprintf("%.3f", $scy[$i*36+1]).' ';
	#print 'L '.sprintf("%.3f", $scx[$i*4+4]).' '.sprintf("%.3f", $scy[$i*4+4]).' ';
	print 'A '.sprintf("%.3f", $sr).' '.sprintf("%.3f", $sr).' 0 0 1 '.sprintf("%.3f", $scx[(($i+1)*36) % 144]).' '.sprintf("%.3f", $scy[(($i+1)*36) % 144]).' ';
}
print 'Z" stroke="blue" fill="transparent"/>'."\n";

print '<path transform="translate(240)" d="M '.sprintf("%.3f", $scx[0]).' '.sprintf("%.3f", $scy[0]).' ';
foreach my $i (0..2) {
	print 'L '.sprintf("%.3f", $bcx[$i*36]).' '.sprintf("%.3f", $bcy[$i*36]).' ';
	#print 'L '.sprintf("%.3f", $bcx[$i*4+1]).' '.sprintf("%.3f", $bcy[$i*4+1]).' ';
	print 'A '.sprintf("%.3f", $br).' '.sprintf("%.3f", $br).' 0 0 1 '.sprintf("%.3f", $bcx[$i*36+10]).' '.sprintf("%.3f", $bcy[$i*36+1]).' ';
	print 'L '.sprintf("%.3f", $scx[$i*36+10]).' '.sprintf("%.3f", $scy[$i*36+1]).' ';
	#print 'L '.sprintf("%.3f", $scx[$i*4+4]).' '.sprintf("%.3f", $scy[$i*4+4]).' ';
	print 'A '.sprintf("%.3f", $sr).' '.sprintf("%.3f", $sr).' 0 0 1 '.sprintf("%.3f", $scx[(($i+1)*36) % 144]).' '.sprintf("%.3f", $scy[(($i+1)*36) % 144]).' ';
}
print 'A '.sprintf("%.3f", $sr).' '.sprintf("%.3f", $sr).' 0 0 1 '.sprintf("%.3f", $scx[0]).' '.sprintf("%.3f", $scy[0]).' ';
print 'Z" stroke="red" fill="transparent"/>'."\n";

print<<EOT
</svg>
EOT