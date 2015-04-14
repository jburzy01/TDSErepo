#  Graphics Interface Module using Tkinter
#
#      created by: Jackson, Caleb, Justin
#      date:       14/13/2015

from Tkinter import *
import Potential as Pt
from Range import Range
import WaveFunction as Wf
import Potential
import FiniteDifference
import Visualize
import math

# Tkinter Grid Geometry Manager to organize labels and GUI options
class Layout:
    def __init__(self):
        self.column = 0
        self.row = 0

    def add(self, element):
        element.grid(row=self.row, column=self.column)
        self.row += 1

    def new_column(self):
        self.row = 0
        self.column += 1

# display contains member functions to create GUI elements like labels, spinbox and drop down meun.
def display():
    master = Tk()
    master.wm_title("TDSE Simulator")
    layout = Layout()

    def label(text):
        layout.add(Label(master, text=text))
    # Returns a function which takes no arguments and returns the value of the variable
    def int_var(low, high, default):
        var = IntVar()
        var.set(default)
        layout.add(Spinbox(master, from_=low, to=high, textvariable=var))
        return var.get
    def double_var(low, high, default):
        var = DoubleVar()
        var.set(default)
        layout.add(Spinbox(master, from_=low, to=high, increment=0.01, textvariable=var))
        return var.get
    # Takes in a dictionary of (name, function) pairs and displays a GUI drop down menu to select init function
    def drop_down(dict, default=None):
        selection = StringVar()
        keys = dict.keys()
        if default is None:
            default = keys[0]
        selection.set(default)
        layout.add(OptionMenu(master, selection, *keys))
        return lambda : dict[selection.get()]

    barrier_fun = lambda x : Pt.barrier(float(get_barrier_width()),float(get_barrier_height()))(x)
    crystal_fun = lambda x : Pt.crystal(float(get_crystal_depth()),float(get_crystal_width()))(x)
    traveling_wave_fun = lambda x: Wf.traveling_wave(float(get_energy()))(x) 
    cos_wave_fun = lambda x: Wf.cos_wave(float(get_width()))(x)

    # ------------ COLUMN 1 ------------- #
    label("Algorithm:")
    algorithm_options = {'Algorithm 1': FiniteDifference.solve1, 'Algorithm 2': FiniteDifference.solve2}
    get_algorithm = drop_down(algorithm_options, default='Algorithm 2')

    label("Width:")
    get_width = int_var(0, 10000000, 20)

    label("Width divisions:")
    get_space_divisions = int_var(10, 500, 200)

    label("Simulation time:")
    get_max_time = int_var(5, 150, 10)

    label("Time divisions:")
    get_time_divisions = int_var(10, 2000, 1000)

    layout.new_column()

    # ------------ COLUMN 2 ------------- #
    label("Potential:")
    potential_options = {'KP-Crystal': crystal_fun, 'Harmonic Oscillator': Pt.harmonic_oscillator(), 'Barrier': barrier_fun, 'Infinite Well/Free Particle': Pt.infinite_well(), "Non-Hermitian (Heatmap Only)": Pt.non_hermitian()}
    get_selected_potential = drop_down(potential_options)

    label("Barrier width:")
    get_barrier_width = int_var(1,100000,1)

    label("Barrier height:")
    get_barrier_height = int_var(1,100000000,4)

    label("Crystal width:")
    get_crystal_width = double_var(0,100000, 0.4)

    label("Crystal depth:")
    get_crystal_depth = int_var(1,100000, 5)

    layout.new_column()

    # ------------ COLUMN 3 ------------- #
    label("Travelling gaussian energy:")
    get_energy = double_var(-1000000,1000000, 1)

    label("Initial Wave:")
    wave_options = {'Cosine wave': cos_wave_fun, 'Gaussian': Wf.gaussian_wave(), 'Travelling gaussian': traveling_wave_fun}
    get_selected_wave = drop_down(wave_options)

    label("Initial wave offset:")
    get_wave_offset = int_var(-10000000, 10000000, 0)

    label("Boundary conditions:")
    get_boundary_conditions = drop_down({'Periodic': True, 'Zero': False}, default='Periodic')

    label("Visualization:")
    opt_animation = 0
    opt_heatmap = 1
    viz_options = {'Animation': opt_animation, 'Heatmap': opt_heatmap}
    get_selected_viz = drop_down(viz_options, default='Animation')

    # run_simulation is called when the simulate command is issued. 
    # Program will initialize the solver, the potential and the wave functions from user GUI inputs
    def run_simulation():
        xs = Range(get_space_divisions(), get_width())
        ts = Range(get_time_divisions(), get_max_time())
        potential = Potential.init(xs, xs.center_function(get_selected_potential()))
        psi_init = Wf.init(xs, Wf.offset(xs.center_function(get_selected_wave()), get_wave_offset()))
        psi = get_algorithm()(xs, ts, potential, psi_init, get_boundary_conditions())
        viz = get_selected_viz()
        if viz == opt_animation:
            Visualize.animate_wave(xs,ts,psi,potential)
        if viz == opt_heatmap:
            Visualize.heatmap(psi)
    layout.add(Button(master, text="Simulate", command=run_simulation))
    master.mainloop()
