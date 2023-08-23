#!/usr/bin/perl 
   ##############################################################################################################
#	r2dita.pl
#	========
#
#	Purpose:
#		Generate DITA files from RAML spec
#
#
# 	v 1.0 	- Written by Philip Sharman, 2023-08-02
##############################################################################################################
use strict;
use warnings 'FATAL' => 'all';
use autodie qw(:all);

use v5.38;

use utf8::all;
use feature 'unicode_strings';
binmode STDOUT, ":encoding(UTF-8)";
use warnings qw(FATAL utf8);

use boolean;
use Carp;
use Data::Printer;
use English;
use feature 'say';
use YAML::XS;

use feature 'signatures';
no warnings qw(experimental::signatures);

# Include my utilities
#use lib $ENV{ 'DEV2_DIR' } . "/Perl Scripts/_My_Utilities";
use lib "$ENV{HOME}/MyPerlUtilities";
#use lib $ENV{ 'DEV2_DIR' } . "MyPerlUtilities";
use PHS; 
use strict;
use warnings;
 
my $filename = './templates/template_start.txt';

if (open(my $fh, '+<', $filename)) {
  while (my $row = <$fh>) {
    chomp $row;
    print "$row\n";
  }
} else {
  warn "Could not open file '$filename' $!";
}