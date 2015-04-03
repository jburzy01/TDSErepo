def init(xs, potential_fun):
    return potential_fun(xs.get_values())

def harmonic_oscillator(xs):
    x_max = xs.get_max()
    return lambda x: .5 * (x-(x_max/2))**2
