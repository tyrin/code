#!/usr/local/bin/perl
use strict;
#print "Called::\n";
my $id="$ARGV[0]";
#print "$id";
my $text=$ARGV[1];


$text =~ s/\<code\>/\<codeph\>/g; #code start tag to codeph
$text =~ s/\<\/code\>/\<\/codeph\>/g; #code end tag to codeph
$text =~ s/\<br\>//g; #remove br start tag 
$text =~ s/\<\/br\>//g; # remove br end tag 

$text =~ s/\:\*\*[\h]*([0-9.a-zA-Z]+)/\<\/b><ph id="$id"\>${1}\<\/ph\>/g; #available version end tag, but processed first
$text =~ s/\*\*\:[\h]*([0-9.a-zA-Z]+)/\<\/b> ${1}/g; #if you put the colon outside the asterisks
#$text =~ s/\:\*\*[\h]*([0-9.a-zA-Z]+)/\<\/b> \<ph\>${1}\<\/ph\>/g; #version with ph
$text =~ s/\*\*/\<b\>/g; #available version start 
$text =~ s/\(\*//g; #remove (*
$text =~ s/\*\)//g; #remove *)
$text =~ s/\[\]//g; #remove []
#$text =~ s///g; #remove less than ? Do we really need these in the doc and could it screw up code examples
#$text =~ s///g; #remove greater than ? Do we really need these in the doc and could it screw up code examples
#$text =~ s/$/1$/g;

#$text =~ s///g;
print "$text"
#print "$text"
##?{[++$count]}