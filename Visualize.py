import matplotlib.pyplot as plt
import matplotlib.animation as animation

def heatmap(solution):
    map_val = lambda x : abs(x)**2
    map_row = lambda row : map_val(row)
    prob_density = map_row(solution)
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(prob_density)
    ax.set_aspect('equal')
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

def animate_wave(xs, ts, solution):
    fig = plt.figure()
    plts = []             # get ready to populate this list the Line artists to be plotted
    plt.hold("off")
    for i in range(ts.get_num_divisions()):
        rplot, = plt.plot(solution[i,:].real, 'r')   # this is how you'd plot a single line...
        iplot, = plt.plot(solution[i,:].imag, 'b')   # this is how you'd plot a single line...
        pplot, = plt.plot(abs(solution[i,:]), 'k')   # this is how you'd plot a single line...
        plts.append([rplot, iplot, pplot])           # ... but save the line artist for the animation
    ani = animation.ArtistAnimation(fig, plts, interval=30, repeat_delay=3000)   # run the animation
    plt.show()
