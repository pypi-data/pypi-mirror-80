import numpy as np
import os
import itertools
from tqdm import trange

class unstructuredGridContainer(object):

    def __init__(self, **kwargs):
        self.origin = kwargs.get('origin', [0, 0, 0])
        self.bound = kwargs.get('bound', [127, 127, 127])
        self.resolution = kwargs.get('resolution', [1, 1, 1])
        self.type = kwargs.get('type', 12)
        self.numNodes = 0
        self.numElements = 0
        self.nodeArray = np.empty(())
        self.elementArray = np.empty(())

    def __repr__(self):
        return 'unstructuredGridContainer Object'

    def __str__(self):
        return 'Unstructured Grid Container(origin={}, bound={}, resolution={}, type={:d})'.format(self.origin,
                                                                                                   self.bound,
                                                                                                   self.resolution,
                                                                                                   self.type)

    @property
    def genMesh(self):

        xNumNodes = int((self.bound[0] - self.origin[0] + 1)/self.resolution[0])
        yNumNodes = int((self.bound[1] - self.origin[1] + 1)/self.resolution[1])
        zNumNodes = int((self.bound[2] - self.origin[2] + 1)/self.resolution[2])

        xCoord = np.linspace(self.origin[0], self.bound[0], xNumNodes)
        yCoord = np.linspace(self.origin[1], self.bound[1], yNumNodes)
        zCoord = np.linspace(self.origin[2], self.bound[2], zNumNodes)

        self.numNodes = xNumNodes * yNumNodes * zNumNodes
        self.numElements = (xNumNodes - 1) * (yNumNodes - 1) * (zNumNodes - 1)


        print('正在创建网格......')
        print('共有节点 {} 个，共有单元 {} 个'.format(self.numNodes, self.numElements))

        self.nodeArray = []

        for combination in itertools.product(xCoord, yCoord, zCoord):
            self.nodeArray.append(combination)
        self.nodeArray = np.array(self.nodeArray)
        self.nodeArray[:] = self.nodeArray[:, [2, 1, 0]]

        if self.type == 12:
            self.elementArray = np.zeros([self.numElements, 8])

        for k in trange(zNumNodes - 1):
            for j in range(yNumNodes - 1):
                for i in range(xNumNodes - 1):
                    elementNum = i + j * (xNumNodes - 1) + k * (xNumNodes - 1) * (yNumNodes - 1)
                    self.elementArray[elementNum] = np.array(
                        [k * xNumNodes * yNumNodes + j * xNumNodes + i,
                         k * xNumNodes * yNumNodes + j * xNumNodes + i + 1,
                         k * xNumNodes * yNumNodes + j * xNumNodes + xNumNodes + i + 1,
                         k * xNumNodes * yNumNodes + j * xNumNodes + xNumNodes + i,
                         k * xNumNodes * yNumNodes + j * xNumNodes + xNumNodes * yNumNodes + i,
                         k * xNumNodes * yNumNodes + j * xNumNodes + xNumNodes * yNumNodes + i + 1,
                         k * xNumNodes * yNumNodes + j * xNumNodes + xNumNodes * yNumNodes + xNumNodes + i + 1,
                         k * xNumNodes * yNumNodes + j * xNumNodes + xNumNodes * yNumNodes + xNumNodes + i,
                         ])
        self.elementArray = self.elementArray.astype(int)

        print('网格创建成功')

        return self.nodeArray, self.elementArray


    def loadMesh(self):
        pass


    def fetchData(self):
        pass

    def writeData(self):
        pass

    def closef(self):
        pass


