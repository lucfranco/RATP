#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import datetime
from dotenv import load_dotenv
from class_base_mariadb import gestionMARIADB
from py2neo import Graph, Node, Relationship

def addslashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)

if __name__ == "__main__":
    load_dotenv(verbose=True)

    # Config MariaDB--------------------------------
    mariadb_config = {
        'user': os.getenv("mariadb_user"),
        'passwd': os.getenv("mariadb_pass"),
        'host': os.getenv("mariadb_host"),
        'database': os.getenv("mariadb_base")
    }

    # Config Neo4j----------------------------------
    neo4j_config = {
        'uri': os.getenv("neo4j_uri"),
        'user': os.getenv("neo4j_user"),
        'pass': os.getenv("neo4j_pass")
    }

    # INIT Neo4j------------------------------------
    graph = Graph(neo4j_config['uri'], auth=(neo4j_config['user'], neo4j_config['pass']))

    # INIT MariaDB------------------------------------
    ratp = gestionMARIADB(mariadb_config)

    # RAZ neo4j--------------------------------
    graph.run("MATCH (n) DETACH DELETE n")

    # INSERT Neo4j List tation---------------------
    listStop = ratp.listStop()
    for stop in listStop:
        request_graph = "CREATE (station:Stop {name: '" + addslashes(str(stop[1])) + "', stop_nom: '" + addslashes(str(stop[2])) + "', stop_desc: '" + addslashes(str(stop[3])) + "', lat: '" + addslashes(str(stop[4])) + "', lon: '" + addslashes(str(stop[5])) + "'})"
        print(request_graph)
        graph.run(request_graph)

    # Extraction RouteGlobal (Unique)
    listRouteGlobal = ratp.extractRouteGlobal()
    nb_route_global = ratp.nb_route_global
    for route_global in listRouteGlobal:
        print(f'extractRouteGlobal {ratp.nb_route_global} {30 * "="}')
        request_graph = "CREATE (:RouteGlobal {id: '" + addslashes(str(route_global[0])) + "', name: '" + addslashes(str(route_global[1])) + "'})"
        print("1| " + request_graph)
        graph.run(request_graph)
        # Extraction ID RouteGlobal---------------------
        listRoute = ratp.extractRoute(addslashes(route_global[1]))
        for route in listRoute:
            print(f'extractRoute {ratp.nb_route} {30 * "="}')
            request_graph = "CREATE (:Route {id: '" + addslashes(str(route[0])) + "', name: '" + addslashes(str(route[1])) + "', long_name: '" + addslashes(str(route[2])) + "', type: '" + addslashes(str(route[3])) + "', route_global: '" + addslashes(str(route_global[1])) + "'})"
            request_graph_01 = "MATCH (rg:RouteGlobal),(r:Route) WHERE rg.id = '" + addslashes(str(route_global[0])) + "' AND r.id = '" + addslashes(str(route[0])) + "' AND r.route_global = '" + addslashes(str(route_global[1])) + "' CREATE (rg)-[:SERVICE]->(r)"
            print("2|- " + request_graph)
            print("2|- " + request_graph_01)
            graph.run(request_graph)
            graph.run(request_graph_01)
            # Extraction Trip---------------------------
            listTrip = ratp.extractTrip(route[1])
            tmp_trip = 1
            for trip in listTrip:
                print(f'extractTrip {tmp_trip}/{ratp.nb_trip} {30 * "="}')
                trajet = ('ALLER' if trip[3] == '0' else 'RETOUR')
                request_graph = "CREATE (:Voyage {id: '" + addslashes(str(trip[0])) + "', name: '" + addslashes(str(trip[1])) + "', short_name: '" + addslashes(str(trip[2])) + "', direction: '" + addslashes(str(trip[3])) + "', route: '" + addslashes(str(route[1])) + "'})"
                request_graph_01 = "MATCH (r:Route),(v:Voyage) WHERE r.id = '" + addslashes(str(route[0])) + "' AND v.id = '" + addslashes(str(trip[0])) + "' AND v.route = '" + addslashes(str(route[1])) + "' CREATE (r)-[:" + trajet + "]->(v)"
                print(f'{tmp_trip} 3|-- {request_graph}')
                print(f'{tmp_trip} 3|-- {request_graph_01}')
                graph.run(request_graph)
                graph.run(request_graph_01)
                tmp_trip += 1
                # Extraction Horaire-------------------
                listHoraire = ratp.extractHoraire(trip[1])
                tmp_horaire = 1
                horaire_old = []
                for horaire in listHoraire:
                    print(f'extractHoraire {tmp_horaire}/{ratp.nb_horaire} {30 * "="}')
                    request_graph = "CREATE (:Horaire {id:" + addslashes(str(horaire[0])) + ", name: '" + addslashes(str(horaire[1])) + "', horaire: '" + addslashes(str(horaire[2])) + "', sequence: " + addslashes(str(horaire[4])) + ", voyage: '" + addslashes(str(trip[0])) + "'})"
                    request_graph_01 = "MATCH (v:Voyage),(h:Horaire) WHERE v.id = '" + addslashes(str(trip[0])) + "' AND h.id = '" + addslashes(str(horaire[0])) + "' AND h.voyage = '" + addslashes(str(trip[0])) + "' CREATE (v)-[:HORAIRE]->(h)"
                    if horaire_old:
                        request_graph_old = "MATCH (h:Horaire),(hold:Horaire) WHERE h.id = '" + addslashes(str(horaire[0])) + "' AND h.voyage = '" + addslashes(str(trip[0])) + "' AND hold.id = '" + addslashes(str(horaire_old[0])) + "' AND hold.voyage = '" + addslashes(str(trip[0])) + "' CREATE (hold)-[:NEXTPOINT]->(h)"
                    print(f'{tmp_horaire} 4|--- {request_graph}')
                    print(f'{tmp_horaire} 4|--- {request_graph_01}')
                    if horaire_old:
                        print(f'{tmp_horaire} 4|--- {request_graph_old}')

                    new_requete = graph.begin()
                    val_node = Node('Horaire',id=horaire[0], name=str(horaire[1]), horaire=horaire[2], sequence=horaire[4], voyage=trip[0])
                    new_requete.create(val_node)
                    new_requete.commit()


                    #graph.run(request_graph)
                    graph.run(request_graph_01)
                    if horaire_old:
                        graph.run(request_graph_old)
                    horaire_old = horaire
                    tmp_horaire += 1
                    # Extraction Stop (station)
                    listLinkStop = ratp.extractStop(horaire[1])
                    tmp_stop = 1
                    for linkstop in listLinkStop:
                        print(f'extractStop {tmp_stop}/{ratp.nb_list_stop} {30 * "="}')
                        request_graph_01 = "MATCH (h:Horaire),(s:Stop) WHERE h.name = '" + addslashes(str(horaire[1])) + "' AND h.voyage = '" + addslashes(str(trip[0])) + "' AND s.name = '" + addslashes(str(horaire[1])) + "' CREATE (h)-[:ARRET]->(s)"
                        print(request_graph_01)
                        graph.run(request_graph_01)
                        tmp_stop += 1
    '''
    '''

    # ratp.test('lulu')
    ratp.extractClose()
    print(nb_route_global)

