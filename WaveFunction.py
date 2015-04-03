import numpy as np
import math

def init(xs, wave_fun):
    psi = normalize(wave_fun(xs.get_values()))
    psi[0] = 0.0
    psi[-1] = 0.0
    return psi

def wave_packet(xs):
    x_max = xs.get_max()
    return lambda x: np.cos((np.pi*(x-x_max/2))/10)

def normalize(vector):
    normconst = 0.0
    length = len(vector)
    for i in xrange(length):
        normconst += abs(vector[i])**2
    for i in xrange(length):
        vector[i] = vector[i]/math.sqrt(normconst)
    return vector