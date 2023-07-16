from py2neo import Graph
# from py2neo import GraphService

# graph = Graph(
#     "http://localhost:11008",
#     username="neo4j",
#     password="123456"
# )  # DataStructureKG
graph = Graph('bolt://localhost:7687', user='neo4j', password='12345678')

CA_LIST = {"数据结构": 0, "操作系统": 1, "计算机网络": 2, "计算机组成原理": 3, "C语言": 4, "Python": 5, "Java": 6}
