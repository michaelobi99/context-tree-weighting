import math
import numpy as np
from collections import defaultdict

default = lambda: 2.0
ktEstimate = defaultdict(default)
def ktEstimator(count, bit: int):
    s = sum(count)
    if ktEstimate[s] == 2.0:
        ktEstimate[s] = math.log(count[bit] + 0.5) - math.log(s + 1.0)
    return ktEstimate[s]

class Node():
    def __init__(self, parent = None):
        self.parent = parent
        self.child = [None] * 2
        self.depth = parent.depth + 1 if parent != None else 0
        self.count = [0] * 2
        self.estimatedProb = 0.0
        self.weightedProb = 0.0

class CTW():
    def __init__(self, contextDepth: int = 3, contextBits = None):
        if contextBits == None:
            contextBits = [0] * contextDepth
        self.depth = contextDepth
        self.root = Node()
        self.contextBits = contextBits

    def update(self, bit, reverse, temp):
        logaddexp = lambda a, b: math.log(math.exp(a) + math.exp(b))
        node = self.root
        for i in range(self.depth, -1, -1):
            #go one step deeper
            if i != self.depth:
                last: int = self.contextBits[i]
                if node.child[last] is None:
                    node.child[last] = Node(parent= node)
                node = node.child[last]
            #update node
            if not reverse:
                node.estimatedProb += math.log(node.count[bit] + 0.5) - math.log(sum(node.count) + 1.0)
                #node.estimatedProb += ktEstimator(node.count, bit)
                node.count[bit] += 1
            else:
                node.count[bit] -= 1
                #node.estimatedProb -= ktEstimator(node.count, bit)
                node.estimatedProb -= math.log(node.count[bit] + 0.5) - math.log(sum(node.count) + 1.0)

        #node is leaf
        assert node.depth == self.depth
        node.weightedProb = node.estimatedProb

        #back-propagate
        while node.parent != None:
            node = node.parent
            assert node.depth < self.depth
            pw0 = node.child[0].weightedProb if node.child[0] != None else 0.0
            pw1 = node.child[1].weightedProb if node.child[1] != None else 0.0
            node.weightedProb = math.log(0.5) + np.logaddexp(node.estimatedProb, pw0 + pw1)

        if not temp:
            self.contextBits = self.contextBits[1:]
            self.contextBits.append(bit)

    def getLogPx(self, bit):
        pw = self.root.weightedProb
        #dummy update
        self.update(bit, reverse= False, temp= True)
        pwx = self.root.weightedProb
        #restore
        self.update(bit, reverse=True, temp= True)
        return pwx - pw