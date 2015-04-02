import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

# builds the matrix needed to solve the TDSE
def buildMatrix(numX, numT, V, deltaX, deltaT):
	array = np.zeros((numX,numT), dtype=complex)
	matrix = np.matrix(array)
	matrix[0,0] = 1
	matrix[-1,-1] = 1

	for n in range(1,numT-1):
		for i in range(numX):
			if i==n:
				matrix[n,i] = V[i] - 2/deltaX**2 - 1j/deltaT
			elif abs(i-n) == 1:
				matrix[n,i] = 1/deltaX**2

	return matrix

# solves for psi using the finite difference algorithm
def finiteDifference(numX, numT, deltaX, deltaT, matrix, psi_init):
	psi = np.zeros((numX,numT), dtype=complex)
	psi[:,0] = psi_init

	# boundary conditions
	psi[0,:] = 0
	psi[-1,:] = 0

	for n in range(numT-1):
		psi[n+1,:] = numpy.linalg.solve(matrix, psi[n,:])
		psi[n+1,:] = normalize(psi[n+1,:])

	return psi

# normalizes a given vector
def normalize(vector):
	normconst = 0
	length = len(vector)

	for i in range(length):
		normconst += abs(vector[i])**2

	vector /= normconst

# constructs the initial wave function
def wavePacket(x):
	return math.exp(-(x)**2) + 0J

# run parameters
a=0
b=1
ti=0
tf=1
deltaX=.1
deltaT=.1

# matrix dimensions
numX = int((b-a)/deltaX)
numT = int((tf-ti)/deltaT)

# initialize the wavefunction
psi_init = np.arange(a,b,deltaX)

for i in range(numX):
	psi_init[i] = psi_init[i] + 0J

psi_init = map(wavePacket,psi_init)


# normalize the wavefunction
psi_init = normalize(psi_init)

# set the potential
V = np.zeros(numX)

# build the matrix
mat = buildMatrix(numX,numT,V,deltaX,deltaT)
print mat

# solve for psi
psi = finiteDifference(numX, numT, mat, deltaX, deltaT, psi_init)
print psi


