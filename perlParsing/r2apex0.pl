#!/usr/local/bin/perl
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
use IO::File;

use feature 'signatures';
no warnings qw(experimental::signatures);

# Include my utilities
use lib "$ENV{HOME}/MyPerlUtilities";
#use lib $ENV{ 'DEV2_DIR' } . "/Perl Scripts/_My_Utilities";
use PHS;

##############################################################################################################
###		GLOBALS																							   ###
##############################################################################################################
#my $gInputFile = 'final.03.yaml';
my $gInputFile = 'final.raml';
# my $gOutputFile = 'output.txt';
# globals for XML variables
my $output = new IO::File(">output.xml");
my $writer = XML::Writer->new(OUTPUT => $output, DATA_MODE => 1, DATA_INDENT => 2, );
my $topicId = "mytopicId";
my $title = "mytitle";
my $shortdesc = "myshortdesc";
my $shortdescId = "myshortdescId";
my $metadataId = "mymetadataId";
my $apiVersion = "myapiVersion";
my $reqchat = "myreqchat";
my $methodName = "mymethodName";
my $methodSignature = "mymethodSignature";
my $ftestCode = "myftestCode";
my $varname = "myvarname";
my $parameterName = "myparameterName";
my $returnType = "myreturnType";
my $typeId = "mytypeId";
##############################################################################################################
###     MAIN                                                                                               ###
##############################################################################################################

my $hashRef = readYaml( $gInputFile );
# PHS::showDataStructure($hashRef);

my $ssot = $hashRef->{ '/ssot' };
# PHS::showDataStructure($ssot);

# showKeys($ssot);
# 	1: '/calculated-insights'
# 	2: '/identity-resolutions'
# 	3: '/identity-resolutions/{identityResolution}'
# 	4: '/insight'
# 	5: '/metadata'
# 	6: '/profile'
# 	7: '/query'
# 	8: '/queryv2'
# 	9: '/queryv2/{nextBatchId}'
# 	10: '/segments'
# 	11: '/universalIdLookup'
# 	12: 'displayName'

showDisplayName( $ssot );

my %ssotHash = %{ $ssot };
while ( my ( $key, $itemHashRef ) = each %ssotHash ) {
	next unless ref( $itemHashRef ) eq 'HASH';
	#say '=' x 110;
	#say "URI: $key";
	processUrl( $itemHashRef );
}

#say '=' x 110;
#say "Done.";
# #say "Output is in:";
# #say "\t $gOutputFile";
# PHS::bbedit($gOutputFile);

##############################################################################################################
##      SUBROUTINES                                                                                        ###
##############################################################################################################
sub processUrl ( $urlHashRef ) {

	$title = showDisplayName( $urlHashRef );

	my @keysItem = getKeys( $urlHashRef );
	for my $keyItem ( @keysItem ) {
		# 		#say "keyItem: '$keyItem'";
		my $valueItem = $urlHashRef->{ $keyItem };

		if ( $keyItem =~ /^(delete|get|patch|post|put)$/ ) {
			#say '-' x 40;
			#say "Method: " . uc( $keyItem );
			processMethod( $valueItem );
			#say '-' x 40;

		} elsif ( $keyItem =~ m{/} ) {
			# 			#say "156: $keyItem";
			processUrl( $valueItem );

		} elsif ( $keyItem eq 'displayName' ) {
			# Ignore this. We've already shown it.

		} elsif ( $keyItem eq 'uriParameters' ) {
			processUrlParameters( $valueItem );

		} else {
			#say "* TODO: We need to handle '$keyItem' (Line: " . __LINE__ . ")";
		}
	}
	return;
}

##############################################################################################################
sub processMethod ( $methodHashRef ) {
	#    PHS::showDataStructure( $methodHashRef );

	showDisplayName( $methodHashRef );
	#say "";

	my $description = $methodHashRef->{ 'description' };
	my $body        = $methodHashRef->{ 'body' };
	chomp( $description );

	# TODO: Handle  $methodHashRef->{ 'responses' };
	# TODO: Handle other keys?

	#say "Description: '$description'";
	#say "";

	handleBody( $body );

	return;
}

##############################################################################################################
sub handleBody ( $bodyHashRef ) {
# 	#say "152:";
# 	PHS::showDataStructure( $bodyHashRef );

	my $example = $bodyHashRef->{ 'application/json' }{ 'example' } // '';
	my $type    = $bodyHashRef->{ 'application/json' }{ 'type' } // '';

	# TODO: Are there other keys to handle here?
	# I think we can ignore '(oas-body-name)'.

	#say "Body:"               if ( ( $type ne '' ) && ( $example ne '' ) );
	#say "\tType: '$type'"       if $type ne '';
	#say "\tExample: '$example'" if $example ne '';

	return;
}

##############################################################################################################
sub processUrlParameters ( $urlParametersHashRef ) {
	die unless ref( $urlParametersHashRef ) eq 'HASH';

	#say "URL Parameters:";
	#say "";

	my @keys = getKeys( $urlParametersHashRef );
	for my $key ( @keys ) {
		my $value = $urlParametersHashRef->{ $key };
		$title = "$key";
		#say "$key:";
		processUrlParameter( $value );
	}

	return;
}

##############################################################################################################
sub processUrlParameter ( $urlParameterHashRef ) {
	die unless ref( $urlParameterHashRef ) eq 'HASH';

	my @keys = getKeys( $urlParameterHashRef );
    $writer->xmlDecl('UTF-8');
    $writer->doctype("reference", "-//OASIS//DTD DITA Reference//EN", "reference.dtd");
    $writer->startTag( 'reference', id => $topicId, "xml:lang" => "en-us"); 
    $writer->startTag('title');
    $writer->startTag('codeph', otherprops => "apex_code");
    $writer->characters($title);
    $writer->endTag('codeph');
    $writer->endTag('title');
    # shortdesc
    $writer->startTag('shortdesc');
    $writer->startTag('ph', id => $shortdescId);
    $writer->characters($shortdesc);
    $writer->endTag('ph');
    $writer->endTag('shortdesc');
    $writer->startTag('prolog');
    $writer->startTag('metadata');
    $writer->emptyTag('othermeta', 'content'=> "Apex_Code_Development_Deployment", 'name' => "app_area");
    $writer->emptyTag('othermeta', 'content'=> "aloha mobile sfx", 'name' => "ui_platform");
    $writer->emptyTag('othermeta', 'content'=> "Developer", 'name' => "role");
    $writer->emptyTag('othermeta', 'content'=> "reference", 'name' => "topic_type");
    $writer->endTag('metadata');
    $writer->endTag('prolog');
    $writer->startTag('refbody');
			for my $key ( @keys ) {
		my $value = $urlParameterHashRef->{ $key };
		
		if ( $key eq 'description' ) {
			#say "\tDescription: $value";
			$shortdesc = "$value";
			$shortdescId = "$value";
		} elsif ( $key eq 'type' ) {
			#say "\tType: $value";
			$returnType = "$value";

		} elsif ( $key eq 'required' ) {
			my $string = ( $value ) ? ' yes' : 'no';
			$reqchat = "$string";
			#say "\tRequired: $string";

		} else {
			#say "* 260: We need to handle '$key'";
			PHS::showDataStructure( $value );
		}
		# API version
    $writer->startTag('section');
    $writer->startTag('title');
    $writer->characters('API Version');
    $writer->endTag('title');
    $writer->startTag('p');
    $writer->characters($apiVersion);
    $writer->endTag('p');
    $writer->endTag('section');
    # Requires Chatter
    $writer->startTag('section');
    $writer->startTag('title');
    $writer->characters('Requires Chatter');
    $writer->endTag('title');
    $writer->startTag('p');
    $writer->characters($reqchat);
    $writer->endTag('p');
    $writer->endTag('section');
    # Signature
    $writer->startTag('section');
    $writer->startTag('title');
    $writer->characters("Signature");
    $writer->endTag('title');
    $writer->startTag('p');
    $writer->startTag('codeph', otherprops => "apex_code");
    $writer->characters($methodSignature);
    $writer->endTag('codeph');
    $writer->endTag('p');
    $writer->startTag('codeblock', otherprops => "apex_code", product => "system");
    $writer->characters($ftestCode);
    $writer->endTag('codeblock');
    $writer->endTag('section');
    # Parameters
    $writer->startTag('section');
    $writer->startTag('title');
    $writer->characters("Parameters");
    $writer->endTag('title');
    $writer->startTag('dl');
    $writer->startTag('dlentry');
    $writer->startTag('dt');
    $writer->startTag('varname');
    $writer->characters($varname);
    $writer->endTag('varname');
    $writer->endTag('dt');
    $writer->startTag('dd');
    $writer->dataElement('p',"Type: ");
    $writer->startTag('xref', href => $typeId, otherprops => "nopage");
    $writer->startTag('codeph', otherprops => "apex_code");
    $writer->characters($parameterName);
    $writer->endTag('codeph');
    $writer->endTag('xref');
    $writer->endTag('dd');
    $writer->endTag('dlentry');
    $writer->endTag('dl');
    $writer->endTag('section');
     # Return Value
     $writer->startTag('section');
    $writer->startTag('title');
    $writer->characters('Return Value');
    $writer->endTag('title');
    $writer->startTag('p');
    $writer->startTag('xref', href => $returnType, otherprops => "nopage");
    $writer->startTag('codeph', otherprops => "apex_code");
    $writer->characters($parameterName);
    $writer->endTag('codeph');
    $writer->endTag('xref');
    $writer->endTag('p');
    $writer->endTag('section');
	}
	#say "";

	return;
}

##############################################################################################################
sub readYaml ( $inputFile ) {
	PHS::assertFileExists( $inputFile );

	my $yamlHashRef = YAML::XS::LoadFile( $inputFile );
	return $yamlHashRef;
}

##############################################################################################################
sub getKeys ( $hashRef ) {
	my @keys = sort keys %{ $hashRef };
	return @keys;
}

##############################################################################################################
sub showKeys ( $hashRef ) {
	my @keys = sort keys %{ $hashRef };
	PHS::showArray( \@keys );
	return;
}

##############################################################################################################
sub showDisplayName ( $hashRef ) {
	my $displayName = $hashRef->{ 'displayName' };
	#say $displayName if defined( $displayName );
	return;
}

##############################################################################################################
