#!/usr/bin/perl
#

use warnings;
use strict;


print '<path style="fill:none;stroke:#000055;stroke-width:0.5" d="M 50 100 ';

# Geberrad 2 Umdrehungen
foreach my $t (1..36, 1..36) {
	if ($t < 35) {
		print " v -40 h 5 v 40 h 5 v -5 v 5 h 5 v -5 v 5 h 5 ";
	} else {
		print " v -5 v 5 h 5 v -5 v 5 h 5 v -5 v 5 h 5 v -5 v 5 h 5 ";
	}
}

print ' "/>'."\n";

print '<path style="fill:none;stroke:#000055;stroke-width:0.5" d="M 50 200 ';

# Nockenwellenrad 1 Umdrehung
foreach my $t (1..72) {
	if ($t == 18 or $t == 36 or $t == 54) {
		print " v -40 h 5 v 40 h 5 v -5 v 5 h 5 v -5 v 5 h 5 ";
	} else {
		print " v -5 v 5 h 5 v -5 v 5 h 5 v -5 v 5 h 5 v -5 v 5 h 5 ";
	}
}

print ' "/>'."\n";


print <<EOT;
</svg>

</body>
</html>
EOT

