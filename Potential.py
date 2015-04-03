def init(xs, potential_fun):
    return potential_fun(xs.get_values())

def harmonic_oscillator(x):
    return .5 * x**2
