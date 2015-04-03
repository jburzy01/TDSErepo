from Range import Range
import WaveFunction
import Potential
import FiniteDifference
import Visualize

xs = Range(100, 10)
ts = Range(500, 5)

potential = Potential.init(xs, Potential.harmonic_oscillator(xs))
psi_init = WaveFunction.init(xs, WaveFunction.wave_packet(xs))

psi = FiniteDifference.solve(xs, ts, potential, psi_init)
Visualize.heatmap(psi)
