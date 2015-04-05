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

# See http://mathworld.wolfram.com/SquareWave.html
def crystal(depth):
    def potential(x):
        return (depth/2.0)+depth*math.pow(-1,math.floor(2*x))
    return potential