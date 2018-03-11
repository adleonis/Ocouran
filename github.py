#!/usr/bin/env python3

import requests
from neo4jrestclient.client import GraphDatabase
from py2neo import Graph, authenticate, Node, Relationship

#db = GraphDatabase("http://localhost:7474", username="neo4j", password="swordfish")

# replace 'foobar' with your password
authenticate("localhost:7474", "neo4j", "swordfish")
graph = Graph()
#Organisation's repos
#curl https://api.github.com/orgs/bitcoin/repos

#Project
#curl https://api.github.com/repos/bitcoin/bitcoin

#Project Contributors
#curl https://api.github.com/repos/monero-project/monero/contributors

#User
#curl https://api.github.com/users/

#Users Following 
#https://api.github.com/users/{user}/following

#User again


def get_json(path):
    r = requests.get(path).json()
    return(r)    

def schema_set_project():
    graph = Graph()   
    #Project = graph.labels.create("Project")                         #create a label
    graph.schema.create_uniqueness_constraint('Project', 'name')

def insert_project(jsoninfo):
    keys = [*jsoninfo]
    print(keys)

    project = {}
    newdicts = []
    for key in keys:
            
        if type(jsoninfo[key]) != dict:
            project[key] = jsoninfo[key]
        else:
            newdicts.append(key)
            globals()[key] = jsoninfo[key]
        
    #print('Project:',project)
    #print('Newdicts:',newdicts)
    #print(owner)

    #Create a name field, so its labelled in graph db
    owner['name'] = owner['login']    

    #Create Project Node
    n1 = Node(*project, **project)
    graph.create(n1)
    
    #Create Liscence Node
    l1 = Node(*license,**license)
    graph.create(l1)
    r1 = Relationship(n1, "HasLicense", l1)
    graph.create(r1)
    #Licence, IsLicensed = graph.create(license, (n1, "IsLicensed", 0))
    
    #Create Owner Node
    o1 = Node(*owner,**owner)
    graph.create(o1)
    r2 = Relationship(n1, "OwnedBy", o1)
    graph.create(r2)

    #Owner, OwnedBy = graph.create(owner, (n1, "OwnedeBy", 0))
    
    
    







if __name__ == '__main__':
    #proj = get_json('https://api.github.com/repos/monero-project/monero')
    proj = get_json('https://api.github.com/repos/bitcoin/bitcoin')
    #schema_set_project()
    something = insert_project(proj)
