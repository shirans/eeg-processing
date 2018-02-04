import random
from collections import namedtuple
from glob import glob

import pyglet
from psychopy import visual, core
from pylsl import StreamInfo, StreamOutlet, pylsl

from constants import gray
from experiment import Experiment
from helpers import local_clock, current_milli_time
from logging_configs import getMyLogger

logger = getMyLogger(__name__)


class P300(Experiment):

    def __init__(self, is_full_screen, win_size, targets, nontargets, outlet, frequency=75, time_stimuli_visible=0.5,
                 num_iteration=1):
        self.x = win_size.hight
        self.y = win_size.wide
        self.outlet = outlet
        self.frequency = frequency
        self.time_stimuli_visible = time_stimuli_visible
        win = self.create_visual(is_full_screen, targets, nontargets)
        super(P300, self).__init__(num_iteration, win)

    def create_visual(self, is_full_screen, targets, nontargets):
        if is_full_screen:
            defDisp = pyglet.window.get_platform().get_default_display()
            allScrs = defDisp.get_screens()
            x = allScrs[0].width
            y = allScrs[0].height
        else:
            x = self.x
            y= self.y
        win = visual.Window(size=[x, y], monitor="testMonitor", rgb=gray,
                            fullscr=is_full_screen, allowGUI=True, units="pix")
        self.targets = map(lambda x: visual.ImageStim(win=win, image=x), glob(targets))
        self.nontargets = map(lambda x: visual.ImageStim(win=win, image=x), glob(nontargets))
        logger.info("num targs: {}, num nontargets: {}".format(len(self.targets), len(self.nontargets)))
        return win

    def change_visual(self):

        if random.randint(1, 100) > self.frequency:
            image = random.choice(self.targets)
            marker = 'rare'
        else:
            image = random.choice(self.nontargets)
            logger.info("drawing common")
            marker = 'common'
        size_x = image.size[0]
        size_y = image.size[1]
        image.size = [size_x * (((self.x - 10) * 1.0) / size_x),
                      size_y * (((self.y - 10) * 1.0) / size_y)]
        image.draw()
        self.outlet.push_sample([marker], current_milli_time())

        self.win.flip()
        core.wait(self.time_stimuli_visible)
        self.win.flip()
