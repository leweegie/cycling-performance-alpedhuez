import math
import numpy as np
import scipy
from numpy.random import rand
import sys

class Route(object):

    def __init__(self, gravity, air_density, friction, file):
        self.gravity = gravity
        self.air_density = air_density
        self.friction = friction
        self.slopes = np.loadtxt(file)[:,0]
        self.distances = np.loadtxt(file)[:,1]