# coding=utf-8
from flask import Flask, jsonify, render_template, request, redirect, url_for
from py2neo import Graph, authenticate
import json,re

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
authenticate("localhost:7474", "neo4j", "liu19950717")
graph = Graph()

def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)
    return {"data": data}

def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id), 
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}
    data.update(relationRecord.r.properties)
    return {"data": data}

def buildEdges1(relationRecord):
    data = {"source": str(re.findall(r"start='node/(.*?)'", str(relationRecord[0]))[0]),
            "target": str(re.findall(r"end='node/(.*?)'", str(relationRecord[0]))[0]),
            "relationship": str(re.findall(r"type='(.*?)'", str(relationRecord[0]))[0]),
            "weight":  str(re.findall(r"weight': '(.*?)'", str(relationRecord[0]))[0])}
    return {"data": data}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    global target
    target = request.get_json()["target"]
    return target

@app.route('/search1')
def search1():
    netset = []
    result = []
    query = 'MATCH (n{name:$tar}) RETURN labels(n)'
    for i in target:
        params = dict(tar=i)
        net = str(graph.cypher.execute(query, params))
        p1 = re.compile(r'[[](.*?)[]]', re.S)
        res = re.findall(p1, net)
        result.append(res)
    result = sum(result,[])
    data = {}
    for key in result:
        key = str(key.replace("'", ""))
        netset.append(key)
    for key in netset:
        data[key] = data.get(key, 0) + 1
    return jsonify(nets = data)

@app.route('/select',methods=['POST'])
def select():
    global lab, check
    lab = str(request.get_json()['net'])
    check = str(request.get_json()['check'])
    # return json.dumps(net, ensure_ascii=False)
    return lab, check

@app.route('/graph')
def get_graph():
    # param = dict(label=lab)
    # query_node = 'MATCH (n:$label) RETURN n'
    # query_edge = 'MATCH ()-[r:$label]->() RETURN r'
    # nodes = list(map(buildNodes, graph.cypher.execute(query_node, param)))
    # edges = list(map(buildEdges, graph.cypher.execute(query_edge, param)))
    nodes = []
    edges = []
    # ——————————————————————————————————————————————————————
    if lab=='pam3':
        if check=='selected':
            query = 'MATCH (n:pam3{name:$tar}) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query, params))))
            nodes = sum(nodes, [])
            return jsonify(elements={"nodes": nodes})
        if check=='all':
            nodes.append(list(map(buildNodes, graph.cypher.execute('MATCH (n:pam3) RETURN n'))))
            edges.append(list(map(buildEdges, graph.cypher.execute('MATCH ()-[r:pam3]->() RETURN r'))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
        else:
            query1 = 'MATCH (m:pam3{name:$tar})-[r*..1]-(n) return n'
            query2 = 'MATCH (n:pam3{name:$tar})-[r*..1]-(m) return r'
            query3 = 'MATCH (n:pam3{name:$tar})-[r*..1]-(m) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query1, params))))
                nodes.append(list(map(buildNodes, graph.cypher.execute(query3, params))))
                edges.append(list(map(buildEdges1, graph.cypher.execute(query2, params))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
    # ——————————————————————————————————————————————————————
    elif lab=='r848':
        if check == 'selected':
            query = 'MATCH (n:r848{name:$tar}) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query, params))))
            nodes = sum(nodes, [])
            return jsonify(elements={"nodes": nodes})
        if check == 'all':
            nodes.append(list(map(buildNodes, graph.cypher.execute('MATCH (n:r848) RETURN n'))))
            edges.append(list(map(buildEdges, graph.cypher.execute('MATCH ()-[r:r848]->() RETURN r'))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
        else:
            query1 = 'MATCH (m:r848{name:$tar})-[r*..1]-(n) return n'
            query2 = 'MATCH (n:r848{name:$tar})-[r*..1]-(m) return r'
            query3 = 'MATCH (n:r848{name:$tar})-[r*..1]-(m) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query1, params))))
                nodes.append(list(map(buildNodes, graph.cypher.execute(query3, params))))
                edges.append(list(map(buildEdges1, graph.cypher.execute(query2, params))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
    # ——————————————————————————————————————————————————————
    elif lab=='I2D':
        if check == 'selected':
            query = 'MATCH (n:I2D{name:$tar}) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query, params))))
            nodes = sum(nodes, [])
            return jsonify(elements={"nodes": nodes})
        if check == 'all':
            nodes.append(list(map(buildNodes, graph.cypher.execute('MATCH (n:I2D) RETURN n'))))
            edges.append(list(map(buildEdges, graph.cypher.execute('MATCH ()-[r:I2D]->() RETURN r'))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
        else:
            query1 = 'MATCH (m:I2D{name:$tar})-[r*..1]-(n) return n'
            query2 = 'MATCH (n:I2D{name:$tar})-[r*..1]-(m) return r'
            query3 = 'MATCH (n:I2D{name:$tar})-[r*..1]-(m) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query1, params))))
                nodes.append(list(map(buildNodes, graph.cypher.execute(query3, params))))
                edges.append(list(map(buildEdges1, graph.cypher.execute(query2, params))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
    # ——————————————————————————————————————————————————————
    elif lab=='HumanNet':
        if check == 'selected':
            query = 'MATCH (n:HumanNet{name:$tar}) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query, params))))
            nodes = sum(nodes, [])
            return jsonify(elements={"nodes": nodes})
        if check == 'all':
            nodes.append(list(map(buildNodes, graph.cypher.execute('MATCH (n:HumanNet) RETURN n'))))
            edges.append(list(map(buildEdges, graph.cypher.execute('MATCH ()-[r:HumanNet]->() RETURN r'))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
        else:
            query1 = 'MATCH (m:HumanNet{name:$tar})-[r*..1]-(n) return n'
            query2 = 'MATCH (n:HumanNet{name:$tar})-[r*..1]-(m) return r'
            query3 = 'MATCH (n:HumanNet{name:$tar})-[r*..1]-(m) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query1, params))))
                nodes.append(list(map(buildNodes, graph.cypher.execute(query3, params))))
                edges.append(list(map(buildEdges1, graph.cypher.execute(query2, params))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
    # ——————————————————————————————————————————————————————
    else:
        if check == 'selected':
            query = 'MATCH (n:HumanSignaling{name:$tar}) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query, params))))
            nodes = sum(nodes, [])
            return jsonify(elements={"nodes": nodes})
        if check == 'all':
            nodes.append(list(map(buildNodes, graph.cypher.execute('MATCH (n:HumanSignaling) RETURN n'))))
            edges.append(list(map(buildEdges, graph.cypher.execute('MATCH ()-[r:HumanSignaling]->() RETURN r'))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
        else:
            query1 = 'MATCH (m:HumanSignaling{name:$tar})-[r*..1]-(n) return n'
            query2 = 'MATCH (n:HumanSignaling{name:$tar})-[r*..1]-(m) return r'
            query3 = 'MATCH (n:HumanSignaling{name:$tar})-[r*..1]-(m) return n'
            for i in target:
                params = dict(tar=i)
                nodes.append(list(map(buildNodes, graph.cypher.execute(query1, params))))
                nodes.append(list(map(buildNodes, graph.cypher.execute(query3, params))))
                edges.append(list(map(buildEdges1, graph.cypher.execute(query2, params))))
            nodes = sum(nodes, [])
            edges = sum(edges, [])
    return jsonify(elements={"nodes": nodes, "edges": edges})

@app.route('/info')
def network():
    return render_template('network.html')

if __name__ == '__main__':
    app.run(debug = True)