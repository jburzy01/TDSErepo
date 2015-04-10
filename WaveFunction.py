import numpy as np
import math

def init(xs, wave_fun):
    psi = normalize(wave_fun(xs.get_values()))
    psi[0] = 0.0
    psi[-1] = 0.0
    return psi

def cos_wave():
    return lambda x : np.cos((np.pi*x)/10)

def gaussian_wave():
    return lambda x : np.exp(-x**2)

def traveling_wave(energy):
    k = math.sqrt(2*energy)
    return lambda x : np.exp(1j*k*x-x**2)

def normalize(vector):
    normconst = 0.0
    length = len(vector)
    for i in xrange(length):
        normconst += abs(vector[i])**2
    for i in xrange(length):
        vector[i] = vector[i]/math.sqrt(normconst)
    return vector

def offset(f, offset_amount):
    return lambda x : f(x-offset_amount)
