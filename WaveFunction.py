import numpy as np
import math

def init(xs, wave_fun):
    psi = normalize(wave_fun(xs.get_values()))
    psi[0] = 0.0
    psi[-1] = 0.0
    return psi

def wave_packet(start_x):
    return lambda x : np.cos((np.pi*(x-start_x))/10)

def gaussian_wave(start_x):
    return lambda x : np.exp(-(x-start_x))

def normalize(vector):
    normconst = 0.0
    length = len(vector)
    for i in xrange(length):
        normconst += abs(vector[i])**2
    for i in xrange(length):
        vector[i] = vector[i]/math.sqrt(normconst)
    return vector