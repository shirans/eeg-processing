import traceback
from abc import abstractmethod

import pyglet
import sys
from plotly.figure_factory._annotated_heatmap import np
from psychopy import visual, core, event
from logging_configs import getMyLogger

logger = getMyLogger(__name__)


class Experiment(object):
    def __init__(self, num_iteration, win, lookup_name, inter_stimuli_interval=1):
        self.num_iteration = num_iteration
        self.win = win
        self.inter_stimuli_interval = inter_stimuli_interval
        self.init_test = "Count how many {} appear".format(lookup_name)

    @abstractmethod
    def create_visual(self, **kwargs):
        pass

    @abstractmethod
    def change_visual(self):
        pass

    def start_experiment(self):

        iteration = self.num_iteration
        logger.info("starting experiment with {} iterations ".format(iteration))
        textbox = visual.TextStim(win=self.win, text=self.init_test, pos=[0, 0], height=21, rgb=-1)
        textbox.draw()
        core.wait(3)

        fixation = visual.TextStim(win=self.win, text="+", pos=[0, 0], rgb=-1)
        fixation.ori = 45
        for i in range(0, iteration):
            fixation.draw()
            self.win.flip()
            core.wait(self.inter_stimuli_interval + np.random.rand())
            self.change_visual()
            keys = event.getKeys()
            if 'escape' in keys:
                logger.info("escape hit")
                break
        logger.debug("closing window")
        try:
            self.win.close()
            # core.quit()
            logger.debug("finished start_experiment ")
        except:
            logger.warn("failed to finish:" + traceback.format_exc())
