from abc import abstractmethod

import pyglet
from plotly.figure_factory._annotated_heatmap import np
from psychopy import visual, core, event
from logging_configs import getMyLogger

logger = getMyLogger(__name__)


class Experiment(object):
    def __init__(self, num_iteration, win, inter_stimuli_interval=1):
        self.num_iteration = num_iteration
        self.win = win
        self.inter_stimuli_interval = inter_stimuli_interval

    @abstractmethod
    def create_visual(self, **kwargs):
        pass

    @abstractmethod
    def change_visual(self):
        pass

    def start_experiment(self):

        iteration = self.num_iteration
        logger.info("starting experiment with {} iterations ".format(iteration))
        fixation = visual.TextStim(win=self.win, text="+", pos=[0, 0], rgb=-1)
        fixation.ori = 45
        for i in range(0, iteration):
            fixation.draw()
            self.win.flip()
            logger.debug("waiting out")
            core.wait(self.inter_stimuli_interval + np.random.rand())
            self.change_visual()
            keys = event.getKeys()
            if 'escape' in keys:
                logger.info("escape hit")
                break
        logger.debug("closing window")
        self.win.close()
        core.quit()
        logger.debug("finished start_experiment ")



