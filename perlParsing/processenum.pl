#!/usr/local/bin/perl
use strict;
#print "Called::\n";
my $id="$ARGV[0]";
#print "$id";
my $text=$ARGV[1];

$text =~ s/\[/<ul id="$id"><li>/g; #process open bracket
$text =~ s/['][,]/<\/li>\n/g;#process close item first
$text =~ s/[']/<li>\n/g;#process close item first
$text =~ s/\]/<\/li><\/ul>/g; #process close bracket
###################### TEMPLATES ######################
#$text =~ s///g;