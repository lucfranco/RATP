#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pycurl
import StringIO

response = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere')
c.setopt(c.WRITEFUNCTION, response.write)
c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
c.setopt(c.POSTFIELDS, '@request.json')
c.perform()
c.close()
print response.getvalue()
response.close()

curl
--header "Content-Type: text/xml;charset=UTF-8"
--header "SOAPAction: ACTION_YOU_WANT_TO_CALL"
--data @FILE_NAME
URL_OF_THE_SOAP_WEB_SERVICE_ENDPOINT

curl
--header "Content-Type: text/xml;charset=UTF-8"
--header "SOAPAction:urn:GetVehicleLimitedInfo"
--data @request.xml
http://11.22.33.231:9080/VehicleInfoQueryService.asmx


<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing">
<soapenv:Header>
<wsa:Action>http://www.w3.org/2005/08/addressing/soap/fault</wsa:Action>
</soapenv:Header>
<soapenv:Body>
<soapenv:Fault>
<faultcode></faultcode>
<faultstring>com.ctc.wstx.exc.WstxUnexpectedCharException:
Unexpected character \'g\' (code 103) in prolog; expected \'&lt;\'\n at [row,col {unknown-source}]: [1,1]</faultstring>
<detail />
</soapenv:Fault>
</soapenv:Body>
</soapenv:Envelope>'


'''
import os
import time
import datetime
from dotenv import load_dotenv
from zeep import Client



wsdl = "http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl"
client = Client(wsdl=wsdl)
string_array = client.get_type('ns0:Line')
string_array('RA')
client.service.method(string_array)


client = Client('http://opendata-tr.ratp.fr/wsiv/services/Wsiv')
order_type = client.get_type('ns0:Line')
order = order_type(id='RA')
client.service.submit_order(user_id=1, order=order)



wsdl = os.getenv("api_url")
client = zeep.Client(wsdl=wsdl)
print(client.service.Line('Zeep', 'testzz'))

from zeep import Client
from zeep import xsd

client = Client(os.getenv("api_url"))
order_type = client.get_element('ns0:Order')
order = xsd.AnyObject(
  order_type, order_type(number='1234', price=99))
client.service.submit_something(user_id=1, _value_1=order)

element = client.get_element('ns0:ElementName')
obj = element(item_1='foo')


from zeep import Client, xsd

API_KEY_TEST = 'YOUR_OWN_API_KEY'
WSDL_TEST = 'https://apitest.trafficvance.com/?v3=system.wsdl'

client = Client(WSDL)
header = xsd.Element(
    '{WSDL_TEST}AuthenticateRequest',
    xsd.ComplexType([
        xsd.Element(
            '{WSDL_TEST}apiKey', xsd.String()
        )
    ])
)
header_value = header(apiKey=API_KEY_TEST)

res = client.service.getServerTime(_soapheaders=[header_value])
'''
