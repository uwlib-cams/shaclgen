#!/usr/bin/env python

from rdflib import Graph, Namespace, XSD, RDF, URIRef
import requests
import rdflib
import sys
from collections import Counter, defaultdict




def generate_groups(input_URI, serialization):
    g = rdflib.Graph()
    g.load(input_URI, format=serialization)
    
    class_list = []
    for s,p,o in g.triples( (None,  RDF.type, None) ):
       class_list.append(o)
    class_list = sorted(list(set(class_list)))
    
    tupes = []
    for k in class_list:
        for s,p,o in g.triples((None, RDF.type, k)):
            for s,p1,o1 in g.triples((s, None, None)):
                tupes.append((k,p1))
    tupes = list(set(tupes))
    
    
    c = Counter(x[1] for x in tupes)
    output = [x + ('unique',) if c[x[1]] == 1 else x + ('repeat',) for x in tupes]
    
    return output
            
#generate the triples  
def generate_triples(output):
    triples = ''
    counter = 0
    for statement in output:
        counter = counter + 1
        if '#' in statement[0]:
            name =  statement[0].split("#")[-1]
        else:
            name =  statement[0].split("/")[-1]
        #gen node shape
        node_triples = (f"""
    <http://example.org/{name}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#NodeShape> .
    <http://example.org/{name}Shape> <http://www.w3.org/ns/shacl#targetClass> <{statement[0]}> .""")
        if statement[2] == 'unique':
            if '#' in statement[1]:
                prop_name = statement[1].split("#")[-1]
            else:
                prop_name = statement[1].split("/")[-1]
            prop_triples = (f"""
    <http://example.org/{name}Shape> <http://www.w3.org/ns/shacl#property> _:{counter} .
    _:{counter} <http://www.w3.org/ns/shacl#path> <{statement[1]}> . """)
        else:
            if '#' in statement[1]:
                prop_name = statement[1].split("#")[-1]
            else:
                prop_name = statement[1].split("/")[-1]
            prop_triples = (f"""
    <http://example.org/{name}Shape> <http://www.w3.org/ns/shacl#property> <http://example.org/{prop_name}Shape> .
    <http://example.org/{prop_name}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#PropertyShape> .
    <http://example.org/{prop_name}Shape> <http://www.w3.org/ns/shacl#path> <{statement[1]}> .""")  
        triples = triples + node_triples + prop_triples
    return triples
    
    
    
    
#generate the graph
def generate_shacl(triples):
    g = rdflib.Graph()
    
    ### bind namespaces to graph, adding in example for default shape namespaces and shacl for shacl props/classes.
    #for key, uri in args:
    #    g.bind(key, URIRef(uri))
    g.bind('ex', URIRef('http://example.org/'))
    g.bind('sh', URIRef('http://www.w3.org/ns/shacl#'))
    
    g.parse(data= triples, format='nt')
    shapes = g.serialize(format='turtle')
    shapes = shapes.decode("utf-8") 
    return shapes