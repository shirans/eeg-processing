import datetime
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import logging.config

from outlet_helper import CHANNELS_NAMES

logger = logging.getLogger(__name__)

COLORS = ['sandybrown', 'lightseagreen', 'navy', 'indianred', 'orchid']


def roll_with_new_data(data, samples, time_x, time_sample):
    nd_samples = np.array(samples).transpose()
    new_data = np.hstack((data, nd_samples))
    num_samples = len(samples)
    new_time = np.hstack((time_x, np.array(time_sample)))
    # remove the prefix
    return new_data[:, num_samples:], new_time[num_samples:]


def print_time_diff(timestamps):
    from_timestamp = datetime.datetime.fromtimestamp(timestamps[0])
    to_timestamp = datetime.datetime.fromtimestamp(timestamps[- 1])
    print from_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], to_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


class FigInfo:
    def __init__(self, frequency, channels_count, seconds_display=10, figsize_w=10, figsize_h=5,
                 refresh=1000):
        fig = plt.figure(figsize=(figsize_w, figsize_h))
        # plt.ion()
        self.is_running = True
        self.num_seconds_display = seconds_display
        self.frequency = frequency
        self.events_in_plot = int(frequency * seconds_display)
        # self.num_events_per_poll = int(frequency * 4)  # poll 4 seconds of events
        self.num_events_per_poll = int(frequency * 4)  # poll 4 seconds of events
        self.refresh = refresh
        self.channels_count = channels_count
        logger.info("frequency: {} seconds to display: {} num events to display: {} events per poll"
                    .format(self.frequency, self.num_seconds_display, self.events_in_plot,
                            self.num_events_per_poll))

        self.data = np.zeros((channels_count, self.events_in_plot))
        self.time_x = np.zeros(self.events_in_plot)

        # Style
        fig.canvas.mpl_connect('key_press_event', self.on_key)

        # plot each line
        lines = []
        x_time = np.arange(self.events_in_plot)

        yprops = dict(rotation=0,
                      horizontalalignment='right',
                      verticalalignment='center',
                      x=-0.01)

        axprops = dict(yticks=[])

        y_channels = np.zeros((self.events_in_plot, channels_count))
        left = 0.1
        bottom = 0.7
        right = 0.8
        top = 0.15
        for i in range(channels_count):
            ax = fig.add_axes([left, bottom, right, top], **axprops)
            line, = ax.plot(x_time, y_channels[::, i], lw=1, color=COLORS[i])
            ax.set_ylabel(CHANNELS_NAMES[i], **yprops)
            if i == channels_count - 1:
                axprops['sharex'] = ax
                axprops['sharey'] = ax
            else:
                plt.setp(ax.get_xticklabels(), visible=False)
            lines.append(line)
            bottom = bottom - 0.15
        ax.set_xlabel('Time (seconds)')
        self.lines = lines
        self.fig = fig
        self.ax = ax

    def plot(self, stream_details):
        while self.is_running:
            logger.info("updating plot")
            samples, timestamps = stream_details.inlet.pull_chunk(
                timeout=1.0, max_samples=self.num_events_per_poll)

            self.data, self.time_x = roll_with_new_data(self.data, samples, self.time_x, timestamps)

            for ii in range(self.channels_count):
                self.lines[ii].set_data(self.time_x, self.data[ii])


            self.fig.canvas.draw()
            self.ax.relim()  # Recalculate limits
            self.ax.autoscale_view(True, True, True)  # Autoscale
            plt.draw()  # Redraw
            sleep(0.5)

    def on_key(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)

        if event.key == 'q':
            self.is_running = False
