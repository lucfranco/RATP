#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pycurl
from io import StringIO
from io import BytesIO

response = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://opendata-tr.ratp.fr/wsiv/services/Wsiv')
c.setopt(c.WRITEFUNCTION, response.write)
c.setopt(c.HTTPHEADER, ['Content-Type: text/xml;charset=UTF-8','SOAPAction:urn:getLines'])
#c.setopt(pycurl.POST, 1)
c.setopt(c.POSTFIELDS, 'getLines.xml')
c.perform()
c.close()
print(response.getvalue())
response.close()
'''
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
'''
