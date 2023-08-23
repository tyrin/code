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
use File::chdir;
use File::Find;
use File::Copy;
use feature 'signatures';
no warnings qw(experimental::signatures);
# Include Philip's utilities
#use lib $ENV{ 'DEV2_DIR' } . "/Perl Scripts/_My_Utilities";
use lib "$ENV{HOME}/MyPerlUtilities";
#use lib $ENV{ 'DEV2_DIR' } . "MyPerlUtilities";
use PHS; 
use strict;
use warnings;

use Cwd qw();
my $targetdir = Cwd::abs_path();
my $inputpath = $targetdir.'/input/'.$ARGV[0];
my $outputpath = $targetdir.'/output/'.$ARGV[0];
my $inputfile;
my $outputfile;

print "Input file: $inputpath\n";
print "Output file: $outputpath\n";

unless (open $inputfile, '<',  $inputpath) {
   print STDERR "Could not open file $inputpath: $!\n";
   # we return 'undefined', we could also 'die' or 'croak'
   return undef
}
unless (open $outputfile, '+>',  $outputpath) {
   print STDERR "Could not open file '$outputpath': $!\n";
   # we return 'undefined', we could also 'die' or 'croak'
   return undef
}

#sub processtags{
#	my $v = shift;
#	$v = s/\<code\>/\<codeph\>/;
#	$v = s/\<code\>/\<codeph\>/;
#	$v = s/\<\/code\>/\<\/codeph\>/;
#	return $v;
#}

my @contents = <$inputfile>;
	# close file
	close($inputfile);
	foreach my $line (@contents){
		#my $lineout = processtags($line);
		#print $outputfile "$lineout";
		print "$line";
		$line = s/\<code\>/\<codeph\>/;
		print "line2: $line";
}

#while( my $line = <$inputfile>)  {  
#	#$line = s/\<code\>/\<codeph\>/;
#	#$line = s/\<code\>/\<codeph\>/;
#	#$line = s/\<\/code\>/\<\/codeph\>/;
#    print $outputfile $line;    
#    last if $. == 2;
#}

#chomp(my @lines = <$inputfile>);
#for ( @lines ) {
#	s/\<code\>/\<codeph\>/;
#	s/\<\/code\>/\<\/codeph\>/;
#	#s/**/""/;
#}



#print $outputfile "@lines";

#close ($inputfile);
close ($outputfile);
