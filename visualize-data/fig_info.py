import matplotlib.pyplot as plt
import numpy as np

from outlet_helper import CHANNELS_NAMES

COLORS = ['sandybrown', 'lightseagreen', 'navy', 'indianred', 'orchid']


class FigInfo:
    def __init__(self, frequency, channels_count, seconds_display=10, figsize_w=10, figsize_h=5):
        self.is_running = True
        fig = plt.figure(figsize=(figsize_w, figsize_h))
        self.num_seconds_display = seconds_display
        self.events_in_plot = int(frequency * seconds_display)

        # Style
        fig.canvas.mpl_connect('key_press_event', self.on_key)

        # ax.set_yticks(np.arange(len(CHANNELS_NAMES)))
        # ax.set_yticklabels(CHANNELS_NAMES)
        # ax.grid(False)

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

    def on_key(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)

        if event.key == 'q':
            self.is_running = False
