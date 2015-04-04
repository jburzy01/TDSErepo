from Range import Range
import WaveFunction
import Potential
import FiniteDifference
import Visualize

xs = Range(200, 20)
ts = Range(1000, 10)

potential = Potential.init(xs, xs.center_function(Potential.infinite_well()))
psi_init = WaveFunction.init(xs, xs.center_function(WaveFunction.traveling_wave(2,-5.0)))

psi = FiniteDifference.solve(xs, ts, potential, psi_init, 2)
Visualize.animate_wave(xs,ts,psi)
