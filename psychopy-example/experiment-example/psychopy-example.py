#!/usr/bin/env python2

from psychopy import visual, core, event


def change_color(win, keys):
    if 'a' in keys:
        if win.color == 'gray':
            win.color = 'blue'aa
        else:
            win.color = 'gray'
        mywin.update()


mywin = visual.Window([800, 600], monitor="testMonitor", units="deg", color='yellow')
grating = visual.GratingStim(win=mywin, mask="circle", size=3, pos=[-4, 0], sf=3)
fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0, 0], sf=0, rgb=-1)

grating.draw()
fixation.draw()
mywin.update()

for frame in range(200):
    grating.setPhase(0.05, '+')  # advance phase by 0.05 of a cycle
    grating.draw()
    fixation.draw()
    mywin.update()
    key = event.getKeys()
    change_color(mywin, key)


mywin.close()
core.quit()
