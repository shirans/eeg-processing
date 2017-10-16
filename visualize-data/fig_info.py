import traceback

import matplotlib.pyplot as plt
import numpy as np
import logging.config
import seaborn as sns
from helpers import roll_with_new_data
from muse_server.outlet_helper import CHANNELS_NAMES, NUM_EVENTS_PER_POLL

logger = logging.getLogger(__name__)

sns.set_style("whitegrid", {'axes.grid': False})

COLORS = ['sandybrown', 'lightseagreen', 'navy', 'indianred', 'orchid']

class FigInfo:
    def __init__(self, frequency, channels_count, seconds_display=3,
                 figsize_w=10, figsize_h=5, num_events_per_poll=NUM_EVENTS_PER_POLL):
        # set consts
        self.is_running = True
        self.num_seconds_display = seconds_display
        self.frequency_hz = frequency  # for example 256
        self.events_in_plot = int(frequency * seconds_display)
        self.num_events_per_poll = num_events_per_poll  # poll events of 0.25 seconds
        self.channels_count = channels_count
        logger.info("frequency: {} seconds to display: {} num events to display: {} events per poll"
                    .format(self.frequency_hz, self.num_seconds_display, self.events_in_plot,
                            self.num_events_per_poll))

        self.data = np.zeros((channels_count, self.events_in_plot))
        self.time_x = np.zeros(self.events_in_plot)

        self.limits = np.zeros((channels_count, 2))
        # init plot
        self.ax = []
        self.lines = []
        self.x = np.arange(0, seconds_display, (1. / self.events_in_plot) * seconds_display)
        self.yprops = dict(rotation=0, horizontalalignment='right', verticalalignment='center', x=3, fontsize=10)
        self.init_axes(figsize_w, figsize_h)

    def init_axes(self, figsize_w, figsize_h):
        fig = plt.figure(figsize=(figsize_w, figsize_h))
        left, bottom, right, top = 0.1, 0.7, 0.8, 0.15
        axprops = dict(yticks=[])
        for i in range(self.channels_count):
            ax = fig.add_axes([left, bottom, right, top], **axprops)
            line, = ax.plot(self.x, self.data[i], lw=0.6, color=COLORS[i])
            ax.set_ylabel(CHANNELS_NAMES[i], **self.yprops)
            ax.set_ylim([-100, 100])
            if i == 1:
                axprops['sharex'] = ax
                axprops['sharey'] = ax
            if i == self.channels_count - 1:
                ax.set_xlabel('Time (seconds)')
            else:
                plt.setp(ax.get_xticklabels(), visible=False)
            self.ax.append(ax)
            self.lines.append(line)
            bottom = bottom - 0.15

    def update_lines(self, time_x, data):
        try:
            x = self.x
            data = list(data)
            for chan in range(self.channels_count):
                line = self.lines[chan]
                new_data = data[chan]
                # set the new data points
                line.set_ydata(new_data)
                line.set_xdata(x)
                ax = self.ax[chan]
                # check if the first seconds of data is too noisy
                first_second_data = new_data[:int(self.frequency_hz)]
                std = np.std(first_second_data)
                label = ax.set_ylabel("{} \n {:0.3f} ".format(CHANNELS_NAMES[chan], new_data[0]),
                                      **self.yprops)
                if std > 50:
                    label.set_color("red")
                else:
                    label.set_color("black")
                ax.relim()
                ax.autoscale_view()
            deltas = []
            for chan in range(0, len(time_x) - 1):
                if time_x[chan + 1] > 0:
                    deltas.append(time_x[chan] - time_x[chan + 1])
            avg = np.average(deltas)
            if avg > 1.0:
                print "average delay is higher than 1 second: {}".format(avg)
            plt.draw()
        except Exception:
            logger.warn(traceback.format_exc())

    def plot(self, stream_details):
        while self.is_running:
            samples, timestamps = stream_details.inlet.pull_chunk(
                timeout=1.0, max_samples=self.num_events_per_poll)
            self.data, self.time_x = roll_with_new_data(self.data, samples, self.time_x, timestamps)
            self.update_lines(self.time_x, self.data)

    def calc_std(self):
        for i in range(0, self.channels_count):
            one_sec_data = self.data[i, :self.frequency_hz]
            # print "channel:{} mean: {} std:{}".format(CHANNELS_NAMES[i], np.mean(one_sec_data), np.std(one_sec_data))


def on_key(self, event):
    print('you pressed', event.key, event.xdata, event.ydata)

    if event.key == 'q':
        self.is_running = False
