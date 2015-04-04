import numpy as np

def init(xs, potential_fun):
    return np.vectorize(potential_fun)(xs.get_values())

def harmonic_oscillator():
    return lambda x : .5 * x**2

def barrier(width, height):
    return lambda x : height if abs(x) <= (width / 2.0) else 0.0

def infinite_well():
    return lambda x : 0.0
