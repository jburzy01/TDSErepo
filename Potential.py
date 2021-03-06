#  Potential Initializing Module
#
#      created by: Jackson, Caleb, Justin
#      date:       14/13/2015

import numpy as np
import math

def init(xs, potential_fun):
    return np.vectorize(potential_fun)(xs.get_values())

def harmonic_oscillator():
    return lambda x : .5 * x**2

def barrier(width, height):
    return lambda x : height if abs(x) <= (width / 2.0) else 0.0

def infinite_well():
    return lambda x : 0.0

def crystal(depth, width):
    def potential(x):
        if x < 0:
            return 0.0
        else:
            return (math.floor(x/width) % 2) * (-depth)
    return potential

def non_hermitian():
    return lambda x : x+1j*x

