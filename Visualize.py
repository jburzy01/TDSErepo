import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def heatmap(solution):
    map_val = lambda x : abs(x)**2
    map_row = lambda row : map_val(row)
    prob_density = map_row(solution)
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    ax.set_xlabel('x')
    ax.set_ylabel('time')
    plt.imshow(prob_density)
    ax.set_aspect('equal')
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

def animate_wave(xs, ts, solution, potential):
    fig = plt.figure()
    plts = []             # get ready to populate this list the Line artists to be plotted
    plt.hold("off")
    # Get the maximum and minimum values over all of time and space
    maximum = float("-inf")
    minimum = float("inf")
    for i in range(ts.get_num_divisions()):
        for arr in [solution[i,:].real, solution[i,:].imag, abs(solution[i,:])]:
            maximum = max(maximum, max(arr))
            minimum = min(minimum, min(arr))
    # Forces potential 0 to align with 0 on the graph
    rng = min(abs(maximum), abs(minimum))
    # atan rescaling maps all real numbers to a finite range and also
    # preserves whether a value is positive or negative
    potential = np.arctan(potential/5)
    minp = -np.pi/2
    maxp = np.pi/2
    normalized_potential = np.interp(potential, [minp, maxp], [-rng, rng])
    for i in range(ts.get_num_divisions()):
        rplot, = plt.plot(solution[i,:].real, 'r')   # this is how you'd plot a single line...
        iplot, = plt.plot(solution[i,:].imag, 'b')
        pplot, = plt.plot(abs(solution[i,:]), 'k')
        pot, = plt.plot(normalized_potential, 'g')
        plts.append([rplot, iplot, pplot, pot])           # ... but save the line artist for the animation
    ani = animation.ArtistAnimation(fig, plts, interval=30, repeat_delay=3000)   # run the animation
    plt.show()
