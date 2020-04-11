import requests

url="http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'application/soap+xml'}
body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope" xmlns:wsiv="http://www.w3.org/2005/08/addressing" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soapenv:Header/>
    <soapenv:Body>
        <wsiv:getLines>
            <wsiv:line>
                <xsd:id>RA</xsd:id>
            </wsiv:line>
        </wsiv:getLines>
    </soapenv:Body>
</soapenv:Envelope>"""

response = requests.post(url,data=body,headers=headers)
print(response.content)
