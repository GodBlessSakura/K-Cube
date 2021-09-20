# from py2neo import Graph, Node, Relationship
# from config import graph
# graph.run('match (n) detach delete n')
# with open("../raw_data/relation.txt", 'r', encoding='utf-8') as f:
#     for line in f.readlines():
#         rela_array=line.strip("\n").split(",")
#         print(rela_array)
#         graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
#         graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
#         graph.run(
#             "MATCH(e: Person), (cc: Person) \
#             WHERE e.Name='%s' AND cc.Name='%s'\
#             CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
#             RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])
#
#         )
from py2neo import Graph, Node, Relationship
from config import graph
graph.run('match (n) detach delete n')
with open("../raw_data/relation.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        rela_array=line.strip("\n").split("\t")
        print(rela_array)
        if (len(rela_array)==3):
            graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % ("General", rela_array[0]))
            graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % ("General", rela_array[2]))
            graph.run(
                "MATCH(e: Person), (cc: Person) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[2], rela_array[1], rela_array[1])
            )

with open("../raw_data/xxx", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        rela_array=line.strip("\n").split("\t")
        print(rela_array)
        if (len(rela_array)==3):
            graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % ("General", rela_array[0]))
            graph.run("MERGE(p: Class{cate:'%s',Name: '%s'})" % ("General", rela_array[2]))
            graph.run(
                "MATCH(e: Class), (cc: Class) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[2], rela_array[1], rela_array[1])
            )

# graph.run('match (n) detach delete n')
# with open("../raw_data/relation.txt", 'r', encoding='utf-8') as f:
#     for line in f.readlines():
#         rela_array=line.strip("\n").split(",")
#         print(rela_array)
#         if (len(rela_array)==5):
#             graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[3], rela_array[0]))
#             graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
#             graph.run(
#                 "MATCH(e: Person), (cc: Person) \
#                 WHERE e.Name='%s' AND cc.Name='%s'\
#                 CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
#                 RETURN r" % (rela_array[0], rela_array[1], rela_array[2], rela_array[2])
#
#             )
