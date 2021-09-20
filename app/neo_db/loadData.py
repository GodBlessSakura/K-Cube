from config import *
import numpy as np

node = set()
link = set()
node2cate = {}
with open("../raw_data/AI", 'r', encoding='utf-8') as f:
    i = 0
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        print(rela_array)
        if len(rela_array) == 5:
            h, r, t, hc, tc = rela_array[0], rela_array[1], rela_array[2], CA_LIST[rela_array[3]], CA_LIST[rela_array[4]]
            node.add(h)
            node2cate[h] = hc
            node.add(t)
            node2cate[t] = tc
            link.add((h, t))
            i += 1
    print(i)

graph = {}
graph["data"] = []
graph["links"] = []
node = list(node)
link = list(link)
for i in range(len(node)):
    dataitem = {"name": node[i], "category": node2cate[node[i]]}
    graph["data"].append(dataitem)

for i in range(len(link)):
    dataitem = {"source": link[i][0], "target": link[i][1]}
    graph["links"].append(dataitem)


print(graph)
