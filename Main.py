import Gui
import sys
import Potential as Pt
import WaveFunction as Wf
import Visualize
from Range import Range
import FiniteDifference
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt

# performs the computation without the GUI: used for barrier calculation
def compute(energy, width, height):
	space_divisions = 300
	length = 30
	time_divisions = 300
	time = 2
	xs = Range(space_divisions, length)
	ts = Range(time_divisions, time)

	barrier_size = int((length/space_divisions)*width)
	potential = Pt.init(xs, xs.center_function(Pt.barrier(width,height)))
	psi_init = Wf.init(xs, Wf.offset(xs.center_function(Wf.traveling_wave(energy)), -5))
	psi = FiniteDifference.solve2(xs, ts, potential, psi_init, False)
	integrate(psi[200,:], xs, barrier_size)
	Visualize.heatmap(psi)

# determines the fraction of the wave that is transmitted and reflected
def integrate(psi, xs, barrier_size):
	transmitted = 0
	reflected = 0
	for i in range(xs.get_num_divisions()/2 + barrier_size/2):
		reflected += abs(psi[i])**2
	for i in range(xs.get_num_divisions()/2 + barrier_size/2, xs.get_num_divisions()):
		transmitted += abs(psi[i])**2
	print "R = ",
	print reflected
	print "T = ",
	print transmitted

def main(argv):
	if argv[0] == "GUI":
		Gui.display()
	elif argv[0] == "barrier":
		compute(float(argv[1]), float(argv[2]), float(argv[3]))

if __name__ == '__main__':
	main(sys.argv[1:])