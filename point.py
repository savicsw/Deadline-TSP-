from random import *
from math import sqrt
import operator
import re
import numpy
import numpy as np

size = 550

class point(object):
    """定义节点，包括：loc，deadline，destination"""
    def __init__(self, *args, **kwargs):
        variance = 130       #方差
        mu = 275            #均值  
        while True :#坐标正态随机
            p = (int(variance*np.random.randn()+mu),int(variance*np.random.randn()+mu))
            #p = (randint(0,550),randint(0,550))         #均匀分布
            if p[0] >= 0 and p[0] <= size and p[1] >= 0 and p[1] <= size:
                break
            if p[0] < 0 : p = (randint(5,15),p[1])
            if p[0] > 550 :p = (randint(545,549),p[1])
            if p[1] < 0 : p = (p[0],randint(5,15))
            if p[1] > 550 :p = (p[0],randint(545,549))
            break
        self.loc = p

        while True:#deadline 正态随机
            a=int(80*np.random.randn()+200)
            b=int(80*np.random.randn()+400)
            if b-a > 240 and a > 60 :break
        self.deadline = (a,b)
        #print(self.deadline)

        self.destination = randint(0,1)
        return super().__init__(*args, **kwargs)


