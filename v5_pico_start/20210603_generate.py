import math
import sys

#print("test")

cx = 100
cy = 100

sr = 50
br = 55

scx = [cx+sr*math.sin(2*math.pi/144*(i-0.5)) for i in range(143)]
scy = [cy-sr*math.cos(2*math.pi/144*(i-0.5)) for i in range(143)]

# coordinates for big circle
bcx = [cx+br*math.sin(2*math.pi/144*(i-0.5)) for i in range(143)]
bcy = [cy-br*math.cos(2*math.pi/144*(i-0.5)) for i in range(143)]
# print(scx)

print('<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">')

print(f'<path d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
for i in range(34):
    print (f'L {bcx[i*4]:.2f} {bcy[i*4]:.2f} ', end='')
    print (f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i*4+1]:.2f} {bcy[i*4+1]:.2f} ', end='')
    print(f'L {scx[i*4+1]:.2f} {scy[i*4+1]:.2f} ', end='')
    print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[i*4+4]:.2f} {scy[i*4+4]:.2f} ', end='')

print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[0]:.2f} {scy[0]:.2f} ', end='')
print('Z" stroke="green" fill="transparent"/>');


print(f'<path transform="translate(120)" d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
for i in range(4):
    print (f'L {bcx[i*36]:.2f} {bcy[i*36]:.2f} ', end='')
    print (f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i*36+1]:.2f} {bcy[i*36+1]:.2f} ', end='')
    print(f'L {scx[i*36+1]:.2f} {scy[i*36+1]:.2f} ', end='')
    #print(((i+1)*36) % 144, file=sys.stderr)
    print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[((i+1)*36) % 144]:.2f} {scy[((i+1)*36) % 144]:.2f} ', end='')

print('Z" stroke="blue" fill="transparent"/>')

print(f'<path transform="translate(240)" d="M {scx[0]:.2f} {scy[0]:.2f} ', end='')
for i in range(3):
    print(f'L {bcx[i*36]:.2f} {bcy[i*36]:.2f} ', end='')
    print(f'A {br:.2f} {br:.2f} 0 0 1 {bcx[i*36+1]:.2f} {bcy[i*36+1]:.2f} ', end='')
    print(f'L {scx[i*36+1]:.2f} {scy[i*36+1]:.2f} ', end='')
    print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[((i+1)*36) % 144]:.2f} {scy[((i+1)*36) % 144]:.2f} ', end='')

print(f'A {sr:.2f} {sr:.2f} 0 0 1 {scx[0]:.2f} {scy[0]:.2f} ', end='')
print('Z" stroke="red" fill="transparent"/>')

print('</svg>')



#https://realpython.com/python-keywords/

# use strict;
# use warnings;
# use Math::Trig;

#print "hello\n";

#this script generates a gear with 34 tooths and 2 gaps
#parameters are: radius and tooths hight

#print sin(pi()/2);
# my $cx = 100;
# my $cy = 100;

# my $sr = 50;
# my $br = 55;

# my @scx; # small circle x-component
# my @scy; # small circle y-component
# my @bcx; # big circle x-component
# my @bcy; # big circle x-component

# foreach my $i (0..143) {
	# $scx[$i] = $cx+$sr*sin(2*pi()/144*($i-0.5));
	# $scy[$i] = $cy-$sr*cos(2*pi()/144*($i-0.5));
	# $bcx[$i] = $cx+$br*sin(2*pi()/144*($i-0.5));
	# $bcy[$i] = $cy-$br*cos(2*pi()/144*($i-0.5));
# }

#print<<EOT
#<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
#EOT

# print '<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">'."\n";

#foreach my $i (0..143) {
#	print '<circle cx="'.sprintf("%.2f", $scx[$i]).'" cy="'.sprintf("%.2f", $scy[$i]).'" r="1" stroke="red" fill="transparent" stroke-width="1"/>'."\n";
#	print '<circle cx="'.sprintf("%.2f", $bcx[$i]).'" cy="'.sprintf("%.2f", $bcy[$i]).'" r="1" stroke="blue" fill="transparent" stroke-width="1"/>'."\n";
#}

# print '<path d="M '.sprintf("%.2f", $scx[0]).' '.sprintf("%.2f", $scy[0]).' ';
# foreach my $i (0..33) {
	# print 'L '.sprintf("%.2f", $bcx[$i*4]).' '.sprintf("%.2f", $bcy[$i*4]).' ';
	#print 'L '.sprintf("%.2f", $bcx[$i*4+1]).' '.sprintf("%.2f", $bcy[$i*4+1]).' ';
	# print 'A '.sprintf("%.2f", $br).' '.sprintf("%.2f", $br).' 0 0 1 '.sprintf("%.2f", $bcx[$i*4+1]).' '.sprintf("%.2f", $bcy[$i*4+1]).' ';
	# print 'L '.sprintf("%.2f", $scx[$i*4+1]).' '.sprintf("%.2f", $scy[$i*4+1]).' ';
	#print 'L '.sprintf("%.2f", $scx[$i*4+4]).' '.sprintf("%.2f", $scy[$i*4+4]).' ';
	# print 'A '.sprintf("%.2f", $sr).' '.sprintf("%.2f", $sr).' 0 0 1 '.sprintf("%.2f", $scx[$i*4+4]).' '.sprintf("%.2f", $scy[$i*4+4]).' ';
# }
# print 'A '.sprintf("%.2f", $sr).' '.sprintf("%.2f", $sr).' 0 0 1 '.sprintf("%.2f", $scx[0]).' '.sprintf("%.2f", $scy[0]).' ';
# print 'Z" stroke="green" fill="transparent"/>'."\n";


# print '<path transform="translate(120)" d="M '.sprintf("%.2f", $scx[0]).' '.sprintf("%.2f", $scy[0]).' ';
# foreach my $i (0..3) {
	# print 'L '.sprintf("%.2f", $bcx[$i*36]).' '.sprintf("%.2f", $bcy[$i*36]).' ';
	#print 'L '.sprintf("%.2f", $bcx[$i*4+1]).' '.sprintf("%.2f", $bcy[$i*4+1]).' ';
	# print 'A '.sprintf("%.2f", $br).' '.sprintf("%.2f", $br).' 0 0 1 '.sprintf("%.2f", $bcx[$i*36+1]).' '.sprintf("%.2f", $bcy[$i*36+1]).' ';
	# print 'L '.sprintf("%.2f", $scx[$i*36+1]).' '.sprintf("%.2f", $scy[$i*36+1]).' ';
	#print 'L '.sprintf("%.2f", $scx[$i*4+4]).' '.sprintf("%.2f", $scy[$i*4+4]).' ';
	# print 'A '.sprintf("%.2f", $sr).' '.sprintf("%.2f", $sr).' 0 0 1 '.sprintf("%.2f", $scx[(($i+1)*36) % 144]).' '.sprintf("%.2f", $scy[(($i+1)*36) % 144]).' ';
# }
# print 'Z" stroke="blue" fill="transparent"/>'."\n";

# print '<path transform="translate(240)" d="M '.sprintf("%.2f", $scx[0]).' '.sprintf("%.2f", $scy[0]).' ';
# foreach my $i (0..2) {
	# print 'L '.sprintf("%.2f", $bcx[$i*36]).' '.sprintf("%.2f", $bcy[$i*36]).' ';
	#print 'L '.sprintf("%.2f", $bcx[$i*4+1]).' '.sprintf("%.2f", $bcy[$i*4+1]).' ';
	# print 'A '.sprintf("%.2f", $br).' '.sprintf("%.2f", $br).' 0 0 1 '.sprintf("%.2f", $bcx[$i*36+1]).' '.sprintf("%.2f", $bcy[$i*36+1]).' ';
	# print 'L '.sprintf("%.2f", $scx[$i*36+1]).' '.sprintf("%.2f", $scy[$i*36+1]).' ';
	#print 'L '.sprintf("%.2f", $scx[$i*4+4]).' '.sprintf("%.2f", $scy[$i*4+4]).' ';
	# print 'A '.sprintf("%.2f", $sr).' '.sprintf("%.2f", $sr).' 0 0 1 '.sprintf("%.2f", $scx[(($i+1)*36) % 144]).' '.sprintf("%.2f", $scy[(($i+1)*36) % 144]).' ';
# }
# print 'A '.sprintf("%.2f", $sr).' '.sprintf("%.2f", $sr).' 0 0 1 '.sprintf("%.2f", $scx[0]).' '.sprintf("%.2f", $scy[0]).' ';
# print 'Z" stroke="red" fill="transparent"/>'."\n";

# print<<EOT
# </svg>
# EOT