<?php

$location = "http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl=";
$uri      = "http://opendata-tr.ratp.fr/wsiv/services";

$options = array(
    'soap_version' => SOAP_1_2,
    'compression'  => SOAP_COMPRESSION_ACCEPT | SOAP_COMPRESSION_GZIP,
    'encoding'     => 'UTF-8',
    'cache_wsdl'   => WSDL_CACHE_NONE
    );
$client = new SoapClient('Wsiv.wsdl', $options );

#$client = new SoapClient(null, array('location' => $location, 'uri' => $uri));
$params = array('line' => array( 'id' => "RA" ));
$response = $client->getLines($params);

print_r(json_encode($response)); /*
$xmlstring = $client->__doRequest($request, $location, $action, $version);
$clean_xml = str_ireplace(['SOAPENV:', 'NS1:', 'NS2:'], '', $xmlstring);
$xml       = simplexml_load_string($clean_xml);

$return        = $xml->Body->getMissionsNextResponse->return;
$perturbations = array();
$missions      = array();

$station     = $return->argumentStation->name;
$direction   = $return->argumentDirection->name;
$line        = $return->argumentLine->reseau->name.' '.$return->argumentLine->code;


echo "Station $station ($line) en direction de $direction", PHP_EOL;

foreach ($return->perturbations as $perturbation) {
    echo $perturbation->message->text, PHP_EOL;
}
 
foreach ($return->missions as $mission) {
    $id = isset($mission->id) ? $mission->id.' ' : "";
    echo $id, $mission->stations[1]->name, ': ', $mission->stationsMessages;
    echo "\n";
}
 */
