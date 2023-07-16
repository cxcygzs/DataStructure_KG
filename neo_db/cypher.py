from py2neo import Graph, Node, Relationship
import json
# from neo_db.config import graph
graph = Graph("http://localhost:7474", auth=("neo4j", "12345678"))

graph.run('match (p:Concept {name: "数据结构"})-[f:常用算法]->(n:Concept) delete f')

graph.run('match (n:Concept {name:"插入"}) delete n')

graph.run('match (n:Concept {name:"删除"}) delete n')
graph.run('match (n:Concept {name:"更新"}) delete n')
graph.run('match (n:Concept {name:"检索"}) delete n')

graph.run('match (n:Concept {name:"检索"}) delete n')




