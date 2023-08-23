#!/usr/local/bin/perl
use XML::Writer;
use IO::File;
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
my $methodName = "mymethodName";
my $varname = "myvarname";
my $parameterName = "myparameterName";
my $returnType = "myreturnType";

&as_method();


sub as_method {
    $writer->xmlDecl('UTF-8');
    $writer->doctype("reference", "-//OASIS//DTD DITA Reference//EN", "reference.dtd");
    $writer->startTag( 'reference', id => $topicId, "xml:lang" => "en-us"); 
    $writer->startTag('title');
    $writer->startTag('codeph', otherprops => "apex_code");
    $writer->characters('title');
    $writer->endTag('codeph');
    $writer->endTag('title');
    # shortdesc
    $writer->startTag('shortdesc');
    $writer->startTag('ph', id => $shortdescId);
    $writer->characters($shortdesc);
    $writer->endTag('ph');
    $writer->endTag('shortdesc');
    # prolog and metadata
	#<prolog><metadata>
	#   <othermeta content="Apex_Code_Development_Deployment" name="app_area"/>
    #	<othermeta content="aloha mobile sfx" name="ui_platform"/>
    #   <othermeta content="Developer" name="role"/>
    #	<othermeta content="reference" name="topic_type"/>
    #</metadata>
    #</prolog>
    $writer->startTag('prolog');
    $writer->startTag('metadata');
    $writer->emptyTag('othermeta', 'content'=> "Apex_Code_Development_Deployment", 'name' => "app_area");
    $writer->emptyTag('othermeta', 'content'=> "aloha mobile sfx", 'name' => "ui_platform");
    $writer->emptyTag('othermeta', 'content'=> "Developer", 'name' => "role");
    $writer->emptyTag('othermeta', 'content'=> "reference", 'name' => "topic_type");
    $writer->endTag('metadata');
    $writer->endTag('prolog');
    $writer->startTag('refbody');
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
    $writer->dataElement(p,"Type: ");
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
    #<section>
    #  <title>Return Value</title>
    #  <p>Type: <xref href="../output_classes/apex_connectapi_output_cdp_segment_output.xml"
    #      otherprops="nopage"><codeph otherprops="apex_code"
    #      >ConnectApi.CdpSegmentOutput</codeph></xref></p>
    #</section>
    $writer->endTag('refbody');
    $writer->endTag('reference');
    $writer->end();
    $output->close();
}
    
    
sub as_class {
    $writer->xmlDecl('UTF-8');
    $writer->doctype("reference", "-//OASIS//DTD DITA Reference//EN", "reference.dtd");
    $writer->startTag( 'reference', id => content, "xml:lang" => "en-us"); 
    $writer->startTag('title');
    $writer->characters($title);
    $writer->endTag('title');
    $writer->startTag('shortdesc');
    $writer->characters('content');
    $writer->endTag('shortdesc');
    $writer->startTag('prolog');
    $writer->startTag('metadata');
    $writer->emptyTag('othermeta', id => $id, "xml:lang" => "en-us");
      # <othermeta content="reference" name="topic_type"/>
      # <othermeta content="Apex_Code_Development_Deployment" name="app_area"/>
      # <othermeta content="aloha mobile sfx" name="ui_platform"/>
      # <othermeta content="Developer" name="role"/>
      # <othermeta content="EE UE DE DBCOM PXE" name="edition"/>
    # </prolog>
    $writer->endTag('metadata');
    $writer->endTag('prolog');
    $writer->startTag('refbody');
    $writer->startTag('section');
    $writer->startTag('title');
    $writer->characters('content');
    $writer->endTag('title');
    $writer->startTag('p');
    $writer->emptyTag('xref', format => "dita", href => "content");
    $writer->endTag('p');
    $writer->endTag('section');
    $writer->endTag('refbody');
    $writer->endTag('reference');
    $writer->end();
    $output->close();
}

