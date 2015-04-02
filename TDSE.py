import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

# builds the matrix needed to solve the TDSE
def buildMatrix(numX, numT, V, deltaX, deltaT):
	matrix = np.zeros((numX,numT), dtype=complex)
#	matrix = np.matrix(matrix)
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
		psi[n+1,:] = np.linalg.solve(matrix, psi[n,:])
		psi[n+1,:] = normalize(psi[n+1,:])

	return psi

# normalizes a given vector
def normalize(vector):

	normconst = 0
	length = len(vector)

	for i in range(length):
		normconst += abs(vector[i])**2
	for i in range(length):
		vector[i] = vector[i]/math.sqrt(normconst)

	return vector 

# builds the initial wave function
def init_psi(a,numX,deltaX):
	# initialize the wavefunction
	psi_init = np.zeros(numX, dtype=complex)

	x=a
	for i in range(numX):
		psi_init[i] = x
		x+=deltaX

	psi_init = map(wavePacket,psi_init)

	# normalize the wavefunction
	psi_init = normalize(psi_init)

	return psi_init


# constructs the initial wave function
def wavePacket(x):
	return math.exp(-(x)**2)

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

# initialize psi
psi_init = init_psi(a,numX,deltaX)

sm = 0
for i in range(numX):
	sm += abs(psi_init[i])**2

print sm

# set the potential
V = np.zeros(numX)

# build the matrix
mat = buildMatrix(numX,numT,V,deltaX,deltaT)

# solve for psi
psi = finiteDifference(numX, numT, deltaX, deltaT, mat, psi_init)
print psi


