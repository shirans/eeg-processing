import random
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
import numpy
from matplotlib import pyplot

hl, = plt.plot([], [])


def update_line(hl, x, y):
    hl.set_xdata(numpy.append(hl.get_xdata(), x))
    hl.set_ydata(numpy.append(hl.get_ydata(), y))
    ax = pyplot.gca()
    ax.relim()
    ax.autoscale_view()
    plt.draw()


def update():
    i = 0
    while True:
        y = i * random.uniform(0, 1)
        print "plotting:{},{}".format(i, y)
        update_line(hl, i, y)
        i = i + 1
        sleep(1)
    return ln,


plotting_thread = Thread(target=update)
plotting_thread.daemon = False
plotting_thread.start()

plt.show()
