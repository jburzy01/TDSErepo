import numpy as np
import math

def init(xs, wave_fun):
    psi = wave_fun(xs.get_values())
    return psi

def cos_wave():
    return lambda x : np.cos((np.pi*x)/10)

def gaussian_wave():
    return lambda x : np.exp(-x**2)

def traveling_wave(energy):
    sigma = 1.0
    k = math.sqrt(2*energy)
    return lambda x : np.exp((.25)*x*(4*1j*k-x*sigma**2))*math.sqrt(np.pi)*(sigma/(math.sqrt(math.sqrt(2)*(np.pi**(3/2))*sigma)))


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
