import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

# builds the matrix needed to solve the TDSE
def buildMatrix(numX, numT, V, deltaX, deltaT):
	matrix = np.zeros((numX,numX), dtype=complex)
	matrix[0,0] = 1
	matrix[-1,-1] = 1

	for n in range(1,numX-1):
		for i in range(numX):
			if i==n:
				matrix[n,i] = V[i] + 2/deltaX**2 - 1j/deltaT
			elif abs(i-n) == 1:
				matrix[n,i] = -1/deltaX**2

	return matrix

# solves for psi using the finite difference algorithm
def finiteDifference(numX, numT, deltaX, deltaT, matrix, psi_init):
	psi = np.zeros((numT,numX), dtype=complex)
	psi[0,:] = psi_init
	# boundary conditions
	psi[:,0] = 0
	psi[:,-1] = 0

	for n in range(numT-1):
		psi[n+1,:] = np.linalg.solve(matrix, -1j*psi[n,:]/deltaT)
		psi[n+1,0] = 0
		psi[n+1,-1] = 0
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
	psi_init[0] = 0
	psi_init[-1] = 0
	# normalize the wavefunction
	psi_init = normalize(psi_init)

	return psi_init

def buildPotential(a,b,numX,deltaX):
	V = np.zeros(numX)
	x=a

	# harmonic oscillator
	for i in range(numX):
		V[i] = .5*x**2
		x+=deltaX	

	# traingular well
#	for i in range(numX):
#		V[i] = abs(x)
#		x+=deltaX	

	# Kronig Penny Crystal
#	for i in range(numX):
#		V[i] = .5*x**2
#		x+=deltaX	



	return V

# constructs the initial wave function
def wavePacket(x):
	return cmath.exp(-(x+3)**2)
#	return A*cmath.exp(-1j*x) + B*cmath.exp(1j*x)
#	return cmath.cos((np.pi * x)/10)

# run parameters
a=-5
b=5
ti=0
tf=5
deltaX=.1
deltaT=.01

# matrix dimensions
numX = int((b-a)/deltaX)
numT = int((tf-ti)/deltaT)

# initialize psi
psi_init = init_psi(a,numX,deltaX)

# set the potential
V = buildPotential(a,b,numX,deltaX)

# build the matrix
mat = buildMatrix(numX,numT,V,deltaX,deltaT)
#print mat
# solve for psi
psi = finiteDifference(numX, numT, deltaX, deltaT, mat, psi_init)


prob_density = np.zeros((numT,numX))

for n in range(numT):
	for i in range(numX):
		prob_density[n,i] = abs(psi[n,i])**2


fig = plt.figure(figsize=(6, 3.2))

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(prob_density)
ax.set_aspect('equal')

cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()
