#!/usr/local/bin/perl
use strict;
my $line="$ARGV[0]";
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
print "$line";