from config import *
# def query(name):
#     print(name)
#     # if name in kg_db.keys():
#     #     print(name)
#     #     return kg_db[name]
#     data = graph.run(
#         "match(p )-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
#             Union all\
#         match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
#     )
#     data = list(data)
#     json_data = get_json_data(data)
#     for i in json_data["data"]:
#         print(i)
#     for i in json_data["links"]:
#         print(i)
#     print(json_data)
#     return json_data

def query(name):
    name = str(name)
    data = graph.run(
        "match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name)
    )
    data = list(data)
    print(get_json_data(data))
    node = set()
    link = set()
    node2cate = {}
    for i in data:
        h, r, t, hc, tc = i["p.Name"], i["r.relation"], i["n.Name"], CA_LIST[i["p.cate"]], CA_LIST[i["n.cate"]]
        node.add(h)
        node2cate[h] = hc
        node.add(t)
        node2cate[t] = tc
        node.add(r)
        node2cate[r] = tc
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

def query_two(name):

    # kg = {}
    # for i in range(4):
    #     data = graph.run(
    #         "match(p:Person{Name:{%s}}- r -> n return p,r,n" % name
    #     )
    #     kg += list(data)

    # data = graph.run("match (p:Person{name:'%s'})-[r]->(n) WITH p, r, n match (n)-[r2]->(n2) where(n2.name<>p.name) return  p.name, r.relation, n.name, n.name, r2.relation, n2.name, p.cate, n.cate, n.cate, n2.cate\
    #         union\
    #         match (p:Person{name:'%s'})-[r]->(n) WITH p, r, n match (n2)-[r2]->(n) where(n2.name<>p.name) return p.name, r.relation, n.name, n2.name, r2.relation, n.name, p.cate, n.cate, n2.cate, n.cate\
    #         union\
    #         match (p)-[r]->(n:Person{name:'%s'}) WITH p, r, n match (p)-[r2]->(n2) where(n2.name<>n.name) return  p.name, r.relation, n.name, r2.relation, n2.name, p.cate, n.cate, n2.cate\
    #         union\
    #         match (p)-[r]->(n:Person{name:'%s'}) WITH p, r, n match (n2)-[r2]->(p) where(n2.name<>n.name) return p.name, r.relation, n.name, r2.relation, n2.name, p.cate, n.cate, n2.cate" % (name,name, name,name))



    data = graph.run(
        "match(p:Class {Name:'%s'}) -[r]-(n) WITH p, r, n match (n)-[r2]->(n2) return p.Name, r.relation, n.Name, r2.relation, n2.Name, p.cate, n.cate, n2.cate" % (name)
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

    print(KG)


query_two("COMP1011")
