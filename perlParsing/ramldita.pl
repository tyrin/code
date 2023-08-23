#!/usr/bin/perl
# use module
# used to open a template file and print it out to a file.
use Cwd;
use File::chdir;
use File::Find; # this is now File:FindByRegex
use File::Copy;
use XML::Simple;
use XML::Parser;
use warnings;
#use diagnostics;

# get directory names
#my $CWD = 'target';
my $targetdir = getcwd;
print "The current directory is $targetdir\n";
#my $file = "$targetdir/input/cdp-connect-api-RAML-$ARGV[0].0.raml";
print "Start template: $starttemplate\n";
print "End template: $endtemplate\n"

my $start = './templates/template_start.txt';
my $end = './templates/template_end.txt';

if (open(my $fh, '+<', $filename)) {
  while (my $row = <$fh>) {
    chomp $row;
    print "$row\n";
  }
} else {
  warn "Could not open file '$filename' $!";
}


# open start template and read it into an array.

#open(ORIGTS, "+<$starttemplate") or die "Couldn't open: $!"; ;
#open(TS, "+<","$start") or die "Couldn't open: $!"; ;
#@startlines = <ORIGTS>;
## remove the </toc> tag.
#for ( @startlines ) {
#	s/\<\/toc\>/ /;}
#close ORIGTS;

# open end template and read it into an array.
#open(ORIGTE, "+file]/$endtemplate") or die "Couldn't open: $!"; ;
#@endlines = <ORIGTE>;
## remove the </toc> tag.
#for ( @endlines ) {
#	s/\<\/toc\>/ /;}
#close ORIGTE;

# open dita file for writing
#print "============================Javadoc========================\n";
#open(OUTF, ">$targetdir/output/connect_api_resource.xml") or die "Couldn't open: $!"; ;
#	print OUTF "@startlines";
#	print OUTF "@endlines";