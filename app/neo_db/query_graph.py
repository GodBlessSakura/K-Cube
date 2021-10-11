from .config import graph
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
    return data


def query_k(name, k):
    data = graph.run(
        "match(p )-[r]->(n:Class{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
            Union all\
        match(p:Class {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
    )
    data = list(data)
    return data



def all_graph():
    data = graph.run(
        "match(p:Person)-[r]->(n:Person) return  p.Name,r.relation,n.Name,p.cate,n.cate"
    )
    data = list(data)
    return data







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







