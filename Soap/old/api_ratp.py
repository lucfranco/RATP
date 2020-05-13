#test soap
from pysimplesoap.client import SoapClient
client = SoapClient(wsdl='http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl')

#print(client.services)
#Line = {'code': '', 'codeStif': '', 'id': 'RA', 'image': '', 'name': '', 'realm': '', 'reseau': 'rer'}
Line = {'line':{'id':"RA"}}
response = client.getLines(Line)
#print('dummy', response)




#from lxml import etree
#from zeep import Client
#import operator

#wsdl = 'http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl'
#client = Client(wsdl)
#result = client.service.getLines("RA")

#print(result)

#client.service.ping()

#element = client.get_element('ns1:getLines')
#obj = element(line={'id' : 'RA'})

#
## get each operation signature
#for service in client.wsdl.services.values():
#    print("service:", service.name)
#    for port in service.ports.values():
#        operations = sorted(
#            port.binding._operations.values(),
#            key=operator.attrgetter('name'))
#
#        for operation in operations:
#            print("method :", operation.name)
#            print("  input :", operation.input.signature())
#            print()
#    print()

# get a specific type signature by name
#complextype = client.get_type('ns0:CartGetRequest')
#print(complextype.name)
#print(complextype.signature())






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
