from psychopy import visual, core, event

from common.constants import gray
from logging_configs import getMyLogger

logger = getMyLogger(__name__)


class Experiment:
    def __init__(self, duration, is_fullscr=False):
        # self.duration = duration
        # self.info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
        # self.outlet = StreamOutlet(self.info)
        self.win = visual.Window(
            size=[800, 600], monitor="testMonitor", rgb=gray,
            fullscr=is_fullscr, allowGUI=True, units='cm')
        # create a window
        # create some stimuli
        self.stim = visual.GratingStim(win=self.win, mask="circle", size=3, pos=[0, 0], sf=3)
        self.fixation = visual.GratingStim(win=self.win, mask="cross", color='red', size=0.2, pos=[0, 0], sf=0, rgb=-1)
        # pause, so you get a chance to see it!
        logger.info("full screen: {} duration: {}".format(is_fullscr, duration))

    def start(self):
        for frame in range(200):  # this creates a never-ending loop
            self.stim.setPhase(0.05, '+')  # advance phase by 0.05 of a cycle
            self.stim.draw()
            self.fixation.draw()
            self.win.flip()

            if len(event.getKeys()) > 0:
                break
            event.clearEvents()
            core.wait(1.0)

        # cleanup
        self.win.close()
        core.quit()
        # for frame in range(200):
        #     self.stim.setPhase(0.05, '+')
        #     self.stim.draw()
        #     self.fixation.draw()
        #     # self.win.update()
        #     self.win.flip()
        #     core.wait(1.0)
        #     if len(event.getKeys()) > 0:
        #         logger.info("key was pressed. exiting")
        #         break
        #     event.clearEvents()
        #     self.win.update()
