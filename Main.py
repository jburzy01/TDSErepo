from Range import Range
import WaveFunction
import Potential
import FiniteDifference
import Visualize

xs = Range(100, 10)
ts = Range(500, 20)

potential = Potential.init(xs, xs.center_function(Potential.harmonic_oscillator))
psi_init = WaveFunction.init(xs, xs.center_function(WaveFunction.wave_packet))

psi = FiniteDifference.solve(xs, ts, potential, psi_init)
Visualize.heatmap(psi)
