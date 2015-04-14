#  Wave Functions Creation Module
#
#      created by: Jackson, Caleb, Justin
#      date:       14/13/2015

import numpy as np
import math

# Wave Functions will always be normalized when initizalized 
def init(xs, wave_fun):
    psi = normalize(wave_fun(xs.get_values()))  
    return psi

# Ground State
def cos_wave(width):
    return lambda x : np.cos((np.pi*x)/(width))

def gaussian_wave():
    return lambda x : np.exp(-x**2/2)

def traveling_wave(energy):
    k = math.sqrt(2*energy)
    return lambda x : np.exp(1j*k*x-x**2/2)

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
