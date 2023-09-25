#!/usr/local/bin/perl
use strict;
#print "Called::\n";
my $id="$ARGV[0]";
#print "$id";
my $text=$ARGV[1];

###################### PROCESS CODE TAGS ######################
$text =~ s/\<br\>//g; #remove br start tag 
$text =~ s/\<\/br\>//g; # remove br end tag 
$text =~ s/</&lt;/g; #replace open tag with &lt;
$text =~ s/`([^`]*)`/<codeph>${1}<\/codeph>/g; #code start tag to codeph
###################### PROCESS LINKS ######################
#remove type=5, which Oxygen doesn't like
$text =~ s/&type[=]+[0-9]+//g;
#reform markdown link into xref
$text =~ s/\[(.*)\]\((.*)\)/<xref href="${2}">${1}<\/xref>/g;
###################### PROCESS SUBSECTIONS ######################
#Type
$text =~ s/\*\*Type:\*\*(.+)/<ph id="${id}_typename">Type:<\/ph><ph id="${id}_typevalue">${1}\<\/ph>\n/g;
#Available Version
$text =~ s/\*\*Available Version:\*\*(.*)/<ph id="${id}_versionname">Available Version:<\/ph><ph id="${id}_versionvalue">${1}\<\/ph>\n/g;
#Filter Group and Version
$text =~ s/\*\*Filter Group and Version:\*\*(.*)/<ph id="${id}_filtername">Filter Group and Version:<\/ph><ph id="${id}_filtervalue">${1}\<\/ph>\n/g;
#Root XML tag
#find double asterisks followed by anything not a colon and capture it followed by a colon and/or askterisks followed by anything not a newline
$text =~ s/\*\*([^:]+)[:*]+(.*)/<ph id="${id}_name">${1}<\/ph><ph id="${id}_value">${2}\<\/ph>/g;
#if it's just a description, include that in a phrase
$text =~ s/^([^<.]*)/<ph id="${id}_desc">${1}<\/ph>/g;

###################### REMOVE MARKDOWN FORMATTING ######################
$text =~ s/\(\*//g; #remove (*
$text =~ s/\*\)//g; #remove *)
$text =~ s/\[\]//g; #remove []

#$text =~ s/$/1$/g;
###################### TEMPLATES ######################
#$text =~ s///g;
###################### RETURN VALUE TO STDOUT ######################
print "$text"
#print "$text"
##?{[++$count]}