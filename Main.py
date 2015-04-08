import Gui
import sys
import Potential as Pt
import WaveFunction as Wf
import Visualize
from Range import Range
import FiniteDifference

# performs the computation without the GUI: used for barrier calculation
def compute(energy, width, height):
	space_divisions = 500
	length = 50
	time_divisions = 300
	time = 3   
	xs = Range(space_divisions, length)
	ts = Range(time_divisions, time)

	potential = Pt.init(xs, xs.center_function(Pt.barrier(width,height)))

	print potential

	psi_init = Wf.init(xs, Wf.offset(xs.center_function(Wf.traveling_wave(energy)), -5))
	psi = FiniteDifference.solve(xs, ts, potential, psi_init, 2)
	integrate(psi[-1,:], xs, potential)
	Visualize.animate_wave(xs,ts,psi)

# determines the fraction of the wave that is transmitted and reflected
def integrate(psi, xs, potential):
	transmitted = 0
	reflected = 0

#	left = 0
#	right = 0
#	found_left = False
#	found_right = False

#	for i in range(xs.get_num_divisions()):
#		if potential[i] != 0 and not found_left:
#			left = i
#			found_left = True
#		if potential[-i] != 0 and not found_right:
#			right = i
#			found_right = True
#		if found_left and found_right:
#			break

	for i in range(xs.get_num_divisions()/2):
		reflected += abs(psi[i])**2
	for i in range(xs.get_num_divisions()/2, xs.get_num_divisions()):
		transmitted += abs(psi[i])**2

	print reflected
	print transmitted

def main(argv):
    if argv[0] == "GUI":
        Gui.display()
    elif argv[0] == "barrier":
        compute(float(argv[1]), float(argv[2]), float(argv[3])) 

if __name__ == '__main__':
    main(sys.argv[1:])
