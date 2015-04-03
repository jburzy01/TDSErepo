import numpy as np

def init(xs, potential_fun):
    return np.vectorize(potential_fun)(xs.get_values())

def harmonic_oscillator(x):
    return .5 * x**2

def barrier(width, height):
    return lambda x : height if abs(x) <= (width / 2.0) else 0.0