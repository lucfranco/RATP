from zeep import Client

wsdl = "https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl"
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
