from abc import abstractmethod

from plotly.figure_factory._annotated_heatmap import np
from psychopy import visual, core

from logging_configs import getMyLogger

logger = getMyLogger(__name__)


class Experiment(object):
    def __init__(self, num_iteration, win):
        self.num_iteration = num_iteration
        self.win = win

    @abstractmethod
    def create_visual(self, **kwargs):
        pass

    @abstractmethod
    def change_visual(self):
        pass

    @abstractmethod
    def report_event(self):
        pass

    def start_experiment(self):
        iteration = self.num_iteration
        logger.info("starting experiment with {} iterations ".format(iteration))
        fixation = visual.TextStim(win=self.win,text="+", pos=[0, 0], rgb=-1)
        fixation.ori = 45
        for i in range(0, iteration):
            fixation.draw()
            self.win.flip()
            logger.debug("waiting out")
            core.wait(1 + np.random.rand())
            # win.flip()
            self.change_visual()
            logger.debug("finished")
