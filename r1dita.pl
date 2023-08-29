#!/usr/local/bin/perl
   ##############################################################################################################
#	r1dita.pl
#	========
#
#	Purpose:
#		Remove or convert markdown tags from RAML spec.
# To run: perl r1dita.pl cdp-connect-api-RAML-59.0.raml
#
# 	v 1.0 	- Written by Tyrin Avery
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


my @contents = <$inputfile>;
	# close file
	close($inputfile);
	foreach my $line (@contents){
		#$line =~ s/^[\h]+#[^%]*//g; #remove comments after a space (this is so we don't remove the root element)
		$line =~ s/\<code\>/\<codeph\>/g; #code start tag to codeph
		$line =~ s/\<\/code\>/\<\/codeph\>/g; #code end tag to codeph
		$line =~ s/\<br\>//g; #remove br start tag 
		$line =~ s/\<\/br\>//g; # remove br end tag 
		$line =~ s/\:\*\*[\h]*([0-9.a-zA-Z]+)/\<\/b> ${1}/g; #available version end tag, but processed first
		$line =~ s/\*\*\:[\h]*([0-9.a-zA-Z]+)/\<\/b> ${1}/g; #if you put the colon outside the asterisks
		#$line =~ s/\:\*\*[\h]*([0-9.a-zA-Z]+)/\<\/b> \<ph\>${1}\<\/ph\>/g; #version with ph
		$line =~ s/\*\*/\<b\>/g; #available version start 
		$line =~ s/\(\*//g; 
		$line =~ s/\*\)//g; 
		$line =~ s/\[\]//g; 
		#$line =~ s///g; 
		
		print  $outputfile "$line";
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
