#!/Users/tavery/perl5/perlbrew/perls/perl-5.38.0/bin/perl
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

use utf8::all;
use feature 'unicode_strings';
binmode STDOUT, ":encoding(UTF-8)";
use warnings qw(FATAL utf8);

use boolean;
use Carp;
#use Data::Printer;
use English;
use feature 'say';
use YAML::XS;
use XML::Writer;
use XML::Simple;
use XML::LibXML;
use IO::File;

use feature 'signatures';
no warnings qw(experimental::signatures);

# Include my utilities
use lib "$ENV{HOME}/MyPerlUtilities";
#use lib $ENV{ 'DEV2_DIR' } . "/Perl Scripts/_My_Utilities";
use PHS;
