import datetime
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import logging.config
from matplotlib import pyplot
from outlet_helper import CHANNELS_NAMES
import seaborn as sns

logger = logging.getLogger(__name__)

sns.set_style("whitegrid", {'axes.grid': False})
sns.despine(left=True)

COLORS = ['sandybrown', 'lightseagreen', 'navy', 'indianred', 'orchid']

xdata, ydata = [], []


def roll_with_new_data(data, samples, time_x, time_sample):
    nd_samples = np.array(samples).transpose()
    new_data = np.hstack((data, nd_samples))
    num_samples = len(samples)
    new_time = np.hstack((time_x, np.array(time_sample)))
    # remove the prefix
    return new_data[:, num_samples:], new_time[num_samples:]


class FigInfo:
    def __init__(self, frequency, channels_count, seconds_display=3, figsize_w=10, figsize_h=5,
                 refresh=1000):
        # set consts
        self.is_running = True
        self.num_seconds_display = seconds_display
        self.frequency = frequency
        self.events_in_plot = int(frequency * seconds_display)
        self.num_events_per_poll = int(frequency /4)  # poll events of 0.25 seconds
        self.num_events_per_poll = int(4)  # poll 4 seconds of events
        self.refresh = refresh
        self.channels_count = channels_count
        logger.info("frequency: {} seconds to display: {} num events to display: {} events per poll"
                    .format(self.frequency, self.num_seconds_display, self.events_in_plot,
                            self.num_events_per_poll))

        self.data = np.zeros((channels_count, self.events_in_plot))
        self.time_x = np.zeros(self.events_in_plot)

        self.ln, = plt.plot([], [])
        # now figure
        # plt.ion()
        # fig = plt.figure(figsize=(figsize_w, figsize_h))
        #
        # left, bottom, right, top = 0.1, 0.7, 0.8, 0.15
        #
        # axprops = dict(yticks=[])
        # self.ax = fig.add_axes([left, bottom, right, top], **axprops)
        # self.ln, = self.ax.plot([], [], 'ro', animated=True)
        # self.line, = ax.plot(self.time_x, self.data[0], lw=1, color=COLORS[0])

        # init
        # ax.set_xlabel('Time (seconds)')
        # plt.show()
        # self.ax = ax

    def update_line(self, time_x, data):
        x = time_x[-1]
        y = data[0][-1]
        print "x: {}. y: {} , timestamp{}".format(
            x, y, datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        hl = self.ln
        new_data = data[0]
        print "len new data {}".format(len(new_data))
        for i in xrange(len(new_data)):
            if 0 < new_data[i]:
                print "first non zero:" + str(i)
                break
        hl.set_xdata(np.append(hl.get_xdata(), time_x[-1]))
        hl.set_ydata(np.append(hl.get_ydata(), new_data[-1]))
        # hl.set_xdata(time_x)
        # hl.set_ydata(new_data)
        ax = pyplot.gca()
        ax.relim()
        ax.autoscale_view()
        plt.draw()

    def plot(self, stream_details):
        while self.is_running:
            logger.info("updating plot")
            samples, timestamps = stream_details.inlet.pull_chunk(
                timeout=1.0, max_samples=self.num_events_per_poll)

            self.data, self.time_x = roll_with_new_data(self.data, samples, self.time_x, timestamps)
            self.update_line(self.time_x, self.data)
            # self.line.set_data(self.time_x, self.data[0])
            # self.ax.relim()
            # self.ax.autoscale_view()
            # self.ax.set_xlim(self.time_x[0],self.time_x[-1])
            # plt.draw()
            # plt.show()




            # for ii in range(self.channels_count):
            #     self.lines[ii].set_data(self.time_x, self.data[ii])
            #
            # self.fig.canvas.draw()
            # self.ax.relim()  # Recalculate limits
            # self.ax.autoscale_view(True, True, True)  # Autoscale
            # plt.draw()  # Redraw
            sleep(0.05)

    def create_ax(self):
        y_channels = np.zeros((self.events_in_plot, self.channels_count))
        left = 0.1
        bottom = 0.7
        right = 0.8
        top = 0.15

        yprops = dict(rotation=0,
                      horizontalalignment='right',
                      verticalalignment='center',
                      x=-0.01)

        axprops = dict(yticks=[])

        for i in range(self.channels_count):
            ax = self.fig.add_axes([left, bottom, right, top], **axprops)
            line, = ax.plot(self.time_x, y_channels[::, i], lw=1, color=COLORS[i])
            ax.set_ylabel(CHANNELS_NAMES[i], **yprops)
            if i == self.channels_count - 1:
                axprops['sharex'] = ax
                axprops['sharey'] = ax
            else:
                plt.setp(ax.get_xticklabels(), visible=False)
            self.lines.append(line)
            bottom = bottom - 0.15
        ax.set_xlabel('Time (seconds)')
        return ax

    def on_key(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)

        if event.key == 'q':
            self.is_running = False
