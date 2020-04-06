# Class Base Neo4j
from py2neo import Graph


class gestionNEO4J:
    neo4j = ''

    def __init__(self, config):
        self.config = config
        self.neo4j = Graph(self.config['uri'], auth=(self.config['user'], self.config['pass']))

    def read_data(self,request):
        print(request)
        result = self.run(request).data()
        #return result

    def neo4jClose(self):
        print(dir(self))
        self.neo4j.Close()
        print("neo4j close !!")
