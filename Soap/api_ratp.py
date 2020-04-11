#test api
from lxml import etree
from zeep import Client
import operator

wsdl = 'http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl'
client = Client(wsdl)
#client.service.ping()

element = client.get_element('ns1:getLines')
obj = element(line={'id' : 'RA'})

#client.service.getLines(item_line)



#element = client.get_element('ns0:Line')
#obj = element(id='RA')


# get a specific type signature by name
#complextype = client.get_type('ns0:Line')



#from zeep import Client


#wsdl = "http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl"
#client = Client(wsdl=wsdl)
#string_array = client.get_type('ns0:Line')
#string_array('RA')
#client.service.method(string_array)

#client = Client('http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl')
#order_type = client.get_type('ns0:Line')
#order = order_type(id='RA')
#print(client.service.submit_order(user_id=1, order=order))
