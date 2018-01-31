import random
from glob import glob

from psychopy import visual, core

from constants import gray
from experiment import Experiment
from logging_configs import getMyLogger

logger = getMyLogger(__name__)


class P300(Experiment):
    def __init__(self, is_full_screen, targets, nontargets, num_iteration=5):
        self.x = 400
        self.y = 300
        win = self.create_visual(is_full_screen, targets, nontargets)
        super(P300, self).__init__(num_iteration, win)

    def create_visual(self, is_full_screen, targets, nontargets):
        win = visual.Window(size=[self.x, self.y], monitor="testMonitor", rgb=gray,
                            fullscr=is_full_screen, allowGUI=True, units="pix")
        self.targets = map(lambda x: visual.ImageStim(win=win, image=x), glob(targets))
        self.nontargets = map(lambda x: visual.ImageStim(win=win, image=x), glob(nontargets))
        logger.info("num targs: {}, num nontargets: {}".format(len(self.targets), len(self.nontargets)))
        return win

    def change_visual(self):
        if random.randint(1, 100) > 75:
            image = random.choice(self.targets)
            logger.info("drawing rare")
        else:
            image = random.choice(self.nontargets)
            logger.info("drawing common")
        logger.info("draw")
        size_x = image.size[0]
        size_y = image.size[1]
        image.size = [size_x * (((self.x - 10) * 1.0) / size_x),
                      size_y * (((self.y - 10) * 1.0) / size_y)]
        image.draw()

        print("x: {} , y: {}".format(size_x, size_y))
        # image.size = [size_x * 1.5, size_y * 1.5]

        self.win.flip()
        logger.info("wait")
        core.wait(0.5)
        logger.info("flip")
        self.win.flip()
