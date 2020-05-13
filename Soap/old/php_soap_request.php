<?php

















getMissionsNext

$request['getMissionsNext'] = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://wsiv.ratp.fr/xsd" xmlns:wsiv="http://wsiv.ratp.fr">
    <soapenv:Header/>
 <soapenv:Body>
     <wsiv:getMissionsNext>
        <wsiv:station>
            <xsd:line>
                <xsd:id>RB</xsd:id>
            </xsd:line>
            <xsd:name>Lozere</xsd:name>
        </wsiv:station>
        <wsiv:direction>
            <xsd:sens>A</xsd:sens>
        </wsiv:direction>
     </wsiv:getMissionsNext>
 </soapenv:Body>
</soapenv:Envelope>';
