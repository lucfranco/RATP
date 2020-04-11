#test api
from zeep import Client
import operator

wsdl = 'http://opendata-tr.ratp.fr/wsiv/services/Wsiv?wsdl'
client = Client(wsdl)

# get each operation signature
for service in client.wsdl.services.values():
    print("service:", service.name)
    for port in service.ports.values():
        operations = sorted(
            port.binding._operations.values(),
            key=operator.attrgetter('name'))

        for operation in operations:
            print("method :", operation.name)
            print("  input :", operation.input.signature())
            print()
    print()

# get a specific type signature by name
complextype = client.get_type('ns0:Line')
print(complextype.name)
print(complextype.signature())



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
