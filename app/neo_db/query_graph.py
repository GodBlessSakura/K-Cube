from .config import graph, CA_LIST, similar_words, kg_db
# from spider.show_profile import get_profile
import codecs
import os
import json
import base64


# cypher

def query():
    data = graph.run(
        "match(p:Class)-[r]->(n:Class) return  p.Name,r.relation,n.Name,p.cate,n.cate"
    )
    data = list(data)
    json_data = get_json_data(data)
    for i in json_data["data"]:
        print(i)
    for i in json_data["links"]:
        print(i)
    # print(get_json_data(data))
    return json_data


def query_k(name, k):
    data = graph.run(
        "match(p )-[r]->(n:Class{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
            Union all\
        match(p:Class {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
    )
    data = list(data)
    print(get_json_data(data))
    return get_json_data(data)


def get_json_data2(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.name"], i["r.relation"], i["n.name"], i["p.cate"], i["n.cate"])
        d.append(i['p.name'] + "_" + i['p.cate'])
        d.append(i['n.name'] + "_" + i['n.cate'])
        d.append(i['n2.name'] + "_" + i['n2.cate'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = i['p.name']

        link_item['target'] = i['n.name']
        link_item['value'] = i['r.relation']
        link_item1 = {}

        link_item1['source'] = i['n.name']

        link_item1['target'] = i['n2.name']
        link_item1['value'] = i['r2.relation']
        json_data['links'].append(link_item1)

    return json_data

def all_graph():
    data = graph.run(
        "match(p:Person)-[r]->(n:Person) return  p.Name,r.relation,n.Name,p.cate,n.cate"
    )
    data = list(data)
    json_data = get_json_data(data)
    for i in json_data["data"]:
        print(i)
    for i in json_data["links"]:
        print(i)
    # print(get_json_data(data))
    return json_data


def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name'] + "_" + i['p.cate'])
        d.append(i['n.Name'] + "_" + i['n.cate'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = name_dict[i['p.Name']]

        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data


def query_11(name):
    data = graph.run(
        "match(p:Class {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name)
    )
    data = list(data)
    print(get_json_data(data))
    node = set()
    link = set()
    node2cate = {}
    for i in data:
        h, r, t, hc, tc = i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"]
        node.add(h)
        node2cate[h] = hc
        node.add(t)
        node2cate[t] = tc
        link.add((h, r))
        link.add((r, t))

    KG = {}
    KG["data"] = []
    KG["links"] = []
    node = list(node)
    link = list(link)
    for i in range(len(node)):
        dataitem = {"name": node[i], "category": node2cate[node[i]]}
        KG["data"].append(dataitem)

    for i in range(len(link)):
        dataitem = {"source": link[i][0], "target": link[i][1]}
        KG["links"].append(dataitem)

    print(KG)


def query_add_link(source, target):
    # graph.run(
    #     "match(p:Class {Name:'%s'}) -[r]->(n:Class {Name:'%s'}) delete r" % (source, target)
    # )
    graph.run(
        "MATCH(e: Class), (cc: Class) \
        WHERE e.Name='%s' AND cc.Name='%s'\
        CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
        RETURN r" % (source, target, "relation", "relation")

    )


def query_delete_link(source, target):
    graph.run(
        "match(p:Class {Name:'%s'}) -[r]->(n:Class {Name:'%s'}) delete r" % (source, target)
    )


def query_add_node(source, target):
    # graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % (source, rela_array[0]))
    graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % ("Others", target,))
    graph.run(
        "MATCH(e: Class), (cc: Class) \
        WHERE e.Name='%s' AND cc.Name='%s'\
        CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
        RETURN r" % (source, target, "relation", "relation")

    )


def query_add_head_node(source, target):
    graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % ("Others", source))
    # graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % ("Others", target))
    graph.run(
        "MATCH(e: Class), (cc: Class) \
        WHERE e.Name='%s' AND cc.Name='%s'\
        CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
        RETURN r" % (source, target, "relation", "relation")

    )


def query_add_tail_node(source, target):
    # graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % (source, rela_array[0]))
    graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % ("Others", target))
    graph.run(
        "MATCH(e: Class), (cc: Class) \
        WHERE e.Name='%s' AND cc.Name='%s'\
        CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
        RETURN r" % (source, target, "relation", "relation")

    )


def query_delete_node(source, target):
    graph.run(
        "match(p:Class {Name:'%s'}) -[r]->(n:Class {Name:'%s'}) delete r" % (source, target)
    )
    graph.run(
        "match(p)-[r]-n delete p" % source
    )


def query_delete_head_node(source):
    graph.run(
        "match(p:Class {Name:'%s'}) -[r]-> (n) delete r" % source
    )
    graph.run(
        "match(p)-[r]->(n:Class {Name:'%s'}) delete r" % source
    )

    graph.run(
        "match(p:Class {Name:'%s'}) delete p" % source
    )


def query_delete_tail_node(target):
    graph.run(
        "match(p:Class {Name:'%s'}) -[r]-> (n) delete r" % target
    )
    graph.run(
        "match(p)-[r]->(n:Class {Name:'%s'}) delete r" % target
    )

    graph.run(
        "match(p:Class {Name:'%s'}) delete p" % target
    )



def query_two(name):
    if name in kg_db.keys():
        print(name)
        return kg_db[name]

    # kg = {}
    # for i in range(4):
    #     data = graph.run(
    #         "match(p:Class{Name:{%s}}- r -> n return p,r,n" % name
    #     )
    #     kg += list(data)

    # data = graph.run("match (p:Class{name:'%s'})-[r]->(n) WITH p, r, n match (n)-[r2]->(n2) where(n2.name<>p.name) return  p.name, r.relation, n.name, n.name, r2.relation, n2.name, p.cate, n.cate, n.cate, n2.cate\
    #         union\
    #         match (p:Class{name:'%s'})-[r]->(n) WITH p, r, n match (n2)-[r2]->(n) where(n2.name<>p.name) return p.name, r.relation, n.name, n2.name, r2.relation, n.name, p.cate, n.cate, n2.cate, n.cate\
    #         union\
    #         match (p)-[r]->(n:Class{name:'%s'}) WITH p, r, n match (p)-[r2]->(n2) where(n2.name<>n.name) return  p.name, r.relation, n.name, r2.relation, n2.name, p.cate, n.cate, n2.cate\
    #         union\
    #         match (p)-[r]->(n:Class{name:'%s'}) WITH p, r, n match (n2)-[r2]->(p) where(n2.name<>n.name) return p.name, r.relation, n.name, r2.relation, n2.name, p.cate, n.cate, n2.cate" % (name,name, name,name))



    data = graph.run(
        "match(p:Class {Name:'%s'}) -[r]-(n) WITH p, r, n match (n)-[r2]-(n2) return p.Name, r.relation, n.Name, r2.relation, n2.Name, p.cate, n.cate, n2.cate" % (name)
    )
    # print("data", data)
    data = list(data)
    # print(data)
    # print(get_json_data(data))
    node = set()
    link = set()
    node2cate = {}
    for i in data:
        # print("i", i)
        h, r, t, r2, t2, hc, tc, t2c = i["p.Name"], i["r.relation"], i["n.Name"], i["r2.relation"], i["n2.Name"], CA_LIST[i["p.cate"]], \
                                   CA_LIST[i["n.cate"]], CA_LIST[i["n2.cate"]]
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        node.add(h)
        node2cate[h] = hc
        node.add(t)
        node2cate[t] = tc
        node.add(t2)
        node2cate[t2] = t2c
        link.add((h, t))
        link.add((t, t2))
    # print("link",list(link))
    KG = {}
    KG["data"] = []
    KG["links"] = []
    node = list(node)
    link = list(link)
    for i in range(len(node)):
        dataitem = {"name": node[i], "category": node2cate[node[i]]}
        KG["data"].append(dataitem)

    for i in range(len(link)):
        dataitem = {"source": link[i][0], "target": link[i][1]}
        KG["links"].append(dataitem)

    return KG



