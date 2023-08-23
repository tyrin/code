#!/usr/local/bin/perl
##############################################################################################################
#	Test 01
#	========
#
#	Purpose:
#		Extract data from RAML.
#
#
# 	v 1.0 	- Written by Philip Sharman, 2023-08-02
##############################################################################################################
use strict;
use warnings 'FATAL' => 'all';
use autodie qw(:all);

use v5.36;

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
use lib $ENV{ 'DEV2_DIR' } . "/Perl Scripts/_My_Utilities";
use PHS;

##############################################################################################################
###		GLOBALS																							   ###
##############################################################################################################
my $gInputFile = 'final.03.yaml';

# my $gOutputFile = 'output.txt';

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
	say '=' x 110;
	say "URI: $key";
	processUrl( $itemHashRef );
}

say '=' x 110;
say "Done.";
# say "Output is in:";
# say "\t $gOutputFile";
# PHS::bbedit($gOutputFile);

##############################################################################################################
##      SUBROUTINES                                                                                        ###
##############################################################################################################
sub processUrl ( $urlHashRef ) {

	showDisplayName( $urlHashRef );

	my @keysItem = getKeys( $urlHashRef );
	for my $keyItem ( @keysItem ) {
		# 		say "keyItem: '$keyItem'";
		my $valueItem = $urlHashRef->{ $keyItem };

		if ( $keyItem =~ /^(delete|get|patch|post|put)$/ ) {
			say '-' x 40;
			say "Method: " . uc( $keyItem );
			processMethod( $valueItem );
			say '-' x 40;

		} elsif ( $keyItem =~ m{/} ) {
			# 			say "156: $keyItem";
			processUrl( $valueItem );

		} elsif ( $keyItem eq 'displayName' ) {
			# Ignore this. We've already shown it.

		} elsif ( $keyItem eq 'uriParameters' ) {
			processUrlParameters( $valueItem );

		} else {
			say "* TODO: We need to handle '$keyItem' (Line: " . __LINE__ . ")";
		}
	}

	return;
}

##############################################################################################################
sub processMethod ( $methodHashRef ) {
	#    PHS::showDataStructure( $methodHashRef );

	showDisplayName( $methodHashRef );
	say "";

	my $description = $methodHashRef->{ 'description' };
	my $body        = $methodHashRef->{ 'body' };
	chomp( $description );

	# TODO: Handle  $methodHashRef->{ 'responses' };
	# TODO: Handle other keys?

	say "Description: '$description'";
	say "";

	handleBody( $body );

	return;
}

##############################################################################################################
sub handleBody ( $bodyHashRef ) {
# 	say "152:";
# 	PHS::showDataStructure( $bodyHashRef );

	my $example = $bodyHashRef->{ 'application/json' }{ 'example' } // '';
	my $type    = $bodyHashRef->{ 'application/json' }{ 'type' } // '';

	# TODO: Are there other keys to handle here?
	# I think we can ignore '(oas-body-name)'.

	say "Body:"               if ( ( $type ne '' ) && ( $example ne '' ) );
	say "\tType: '$type'"       if $type ne '';
	say "\tExample: '$example'" if $example ne '';

	return;
}

##############################################################################################################
sub processUrlParameters ( $urlParametersHashRef ) {
	die unless ref( $urlParametersHashRef ) eq 'HASH';

	say "URL Parameters:";
	say "";

	my @keys = getKeys( $urlParametersHashRef );
	for my $key ( @keys ) {
		my $value = $urlParametersHashRef->{ $key };

		say "$key:";
		processUrlParameter( $value );
	}

	return;
}

##############################################################################################################
sub processUrlParameter ( $urlParameterHashRef ) {
	die unless ref( $urlParameterHashRef ) eq 'HASH';

	my @keys = getKeys( $urlParameterHashRef );

	for my $key ( @keys ) {
		my $value = $urlParameterHashRef->{ $key };

		if ( $key eq 'description' ) {
			say "\tDescription: $value";

		} elsif ( $key eq 'type' ) {
			say "\tType: $value";

		} elsif ( $key eq 'required' ) {
			my $string = ( $value ) ? ' yes' : 'no';
			say "\tRequired: $string";

		} else {
			say "* 260: We need to handle '$key'";
			PHS::showDataStructure( $value );
		}
	}
	say "";

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
	say $displayName if defined( $displayName );
	return;
}

##############################################################################################################