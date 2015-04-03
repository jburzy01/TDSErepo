from Range import Range
import WaveFunction
import Potential
import FiniteDifference
import Visualize

xs = Range(100, 10)
ts = Range(500, 20)

potential = Potential.init(xs, xs.center_function(Potential.barrier(0.5, 0.5)))
psi_init = WaveFunction.init(xs, xs.center_function(WaveFunction.gaussian_wave(7.0)))

psi = FiniteDifference.solve(xs, ts, potential, psi_init)
Visualize.heatmap(psi)
