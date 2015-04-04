from Range import Range
import WaveFunction
import Potential
import FiniteDifference
import Visualize

xs = Range(200, 20)
ts = Range(1000, 40)

potential = Potential.init(xs, xs.center_function(Potential.infinite_well()))
psi_init = WaveFunction.init(xs, xs.center_function(WaveFunction.gaussian_wave(0.0)))

psi = FiniteDifference.solve(xs, ts, potential, psi_init, 2)
Visualize.animate_wave(xs,ts,psi)
