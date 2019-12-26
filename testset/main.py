# -*- coding: UTF-8 -*-
import random
import json

class Node:
    id = 0
    type = "default"

    def __init__(self, _id, _type="default"):
        self.id = _id
        self.type = _type

    def todict(self):
        out = {}
        out['id'] = self.id
        out['type'] = self.type
        return out

class Edge:
    source = 0
    target = 0

    def __init__(self, _source, _target):
        self.source = _source
        self.target = _target

    def todict(self):
        out = {}
        out['source'] = self.source
        out['target'] = self.target
        return out


class Graph:
    def __init__(self, obj):
        self.vertex = obj.vertex
        self.edge = obj.edge

# 1.构建 10*10 的网状图
class Network():
    def __init__(self, col, row):
        self.vertex = []
        self.edge = []
        for i in range(0, col):
            for j in range(0, row):
                node = Node(i * 10 + j)
                self.vertex.append(node)
        for i in range(0, col):
            for j in range(0, row):
                if j != row - 1:
                    edgeRight = Edge(
                        self.vertex[i * 10 + j].id, self.vertex[i * 10 + j + 1].id)  # 与右边的连线
                    self.edge.append(edgeRight)
                if i != col - 1:
                    edgeBelow = Edge(
                        self.vertex[i * 10 + j].id, self.vertex[(i + 1) * 10 + j].id)  # 与下面的连线
                    self.edge.append(edgeBelow)


# 2.构建子图
# 2.1 星状 star
class Star():
    def __init__(self, begin, number, gid):
        self.vertex = []
        self.edge = []
        for i in range(0, number):
            node = Node(begin + i, "star_" + str(gid))
            self.vertex.append(node)
        center = random.randint(0, number - 1)  # 随机选择中心
        for i in range(0, number):
            if i != center:
                edge = Edge(self.vertex[center].id, self.vertex[i].id)  # 连接其他点与中心
                self.edge.append(edge)


# 2.2 二部图 bipartite cores
class Bipartite():
    def __init__(self, begin, number, gid):
        self.vertex = []
        self.edge = []
        A = 0
        B = 0
        if number % 2 == 0:
            A = number // 2
            B = number // 2
        else:
            A = number // 2 + 1
            B = number // 2
        for i in range(0, number):
            node = Node(begin + i, "bipartite_" + str(gid))
            self.vertex.append(node)
        #连接 A -> B
        for i in range(0, A):
            for j in range(A, A + B):
                edge = Edge(self.vertex[i].id, self.vertex[j].id)
                self.edge.append(edge)

# 2.3 完全图 cliques
class Cliques():
    def __init__(self, begin, number, gid):
        self.vertex = []
        self.edge = []
        for i in range(0, number):
            node = Node(begin + i, "cliques_" + str(gid))
            self.vertex.append(node)
        for i in range(0, number):
            for j in range(i+1, number): # 防止重复连线
                    edge = Edge(self.vertex[i].id, self.vertex[j].id)
                    self.edge.append(edge)


# 2.4 金氏图 King's graph
class King():
    def __init__(self, begin, number, gid):
        self.vertex = []
        self.edge = []
        col = row = int(number ** 0.5)
        for i in range(0, row):
            for j in range(0, col):
                node = Node(begin + i * col + j, "King's_" + str(gid))
                self.vertex.append(node)
        for i in range(0, row):
            for j in range(0, col):
                if j != col - 1:
                    edgeRight = Edge(
                        self.vertex[i * col + j].id, self.vertex[i * col + j + 1].id)  # 与右边的连线
                    self.edge.append(edgeRight)
                if i != row - 1:
                    edgeBelow = Edge(
                        self.vertex[i * col + j].id, self.vertex[(i + 1) * col + j].id)  # 与下面的连线
                    self.edge.append(edgeBelow)
                    if j != col - 1:
                        edgeBelowRight = Edge( # 与右下角的连线
                            self.vertex[i * col + j].id, self.vertex[(i + 1) * col + j + 1].id)
                        self.edge.append(edgeBelowRight)
                    if j != 0:
                        edgeBelowLeft = Edge( # 与左下角的连线
                            self.vertex[i * col + j].id, self.vertex[(i + 1) * col + j - 1].id)
                        self.edge.append(edgeBelowLeft)


TestSet = {}
use = []
dic = {1: King, 2: Star, 3: Bipartite, 4: Cliques}

    # 子图类型、起始id、节点数、子图编号
def join(gtype, begin, number, gid):
    # 创建子图
    subgraph = dic[gtype](begin, number, gid)
    # 将子图节点、边压入主图
    for v in range(len(subgraph.vertex)):
        TestSet.vertex.append(subgraph.vertex[v])
    for e in range(len(subgraph.edge)):
        TestSet.edge.append(subgraph.edge[e])
    # 主图上选择一点
    connect = use[random.randint(0, len(use) - 1)]
    # 子图上选择一点
    subconnect = subgraph.vertex[random.randint(0, len(subgraph.vertex) - 1)].id
    # 记录连接点
    print connect, subconnect, dic[gtype], gid
    edge = Edge(connect, subconnect)
    TestSet.edge.append(edge)
    # 该点不再使用
    use.remove(connect)


def gen_graph(net):
    out = {}
    out["graph"] = {}
    out["graph"]["vertex"] = []
    out["graph"]["edge"] = []
    D = {}
    for nodetmp in net.edge:
        D = nodetmp.todict()
        out["graph"]['edge'].append(D)
    for nodetmp in net.vertex:
        D = nodetmp.todict()
        out["graph"]["vertex"].append(D)

    return out

TIME = [10, 20, 5]
NODE = [16, 25, 9]

for t in range(0, 3):
    TestSet = Graph(Network(10, 10))  # 3个10*10测试集初始化
    use = range(100)
    for i in range(0, TIME[t]):
        for j in range(1, 5):
            join(j, len(TestSet.vertex), NODE[t], i)
    try:
        #   写回
            file_write = open("testset_"+str(t)+".json", 'w')
            json.dump(gen_graph(TestSet), file_write, indent=4)
            file_write.close()
    except IOError:
        print("文件%s无法写入" % return_name)
