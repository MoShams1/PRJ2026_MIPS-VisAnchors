"""
"""
from psychopy import event, core, visual, monitors
import supplements as sup
import pandas as pd
import numpy as np
import os
import warnings
import random

warnings.simplefilter(action='ignore', category=FutureWarning)

# -------------------------------------------------
# insert session meta data
# -------------------------------------------------
subject = '003'
# -------------------------------------------------
# destination file
# -------------------------------------------------
date = sup.get_date()
time = sup.get_time()
file_name = f"exp03_{subject}_{date}_{time}.json"
data_path = os.path.join('..', 'data', file_name)
# -------------------------------------------------
# initialize display
# -------------------------------------------------
monitor = monitors.Monitor('prim_mon', width=200, distance=180)
monitor.setSizePix([1920, 1080])
win = visual.Window(monitor=monitor,
                    units='deg',
                    size=[1920, 1080],
                    pos=[0, 0],
                    fullscr=True,
                    color='black')
win.mouseVisible = False
refresh_rate = 120
# -------------------------------------------------
# set up task parameters
# -------------------------------------------------
flash_dur_frames = 2  # frames

frame_half_width = 4

motion_path_length = 6  # dva
motion_path_dur_sec = 0.4
motion_path_dur_frames = int(motion_path_dur_sec * refresh_rate)
motion_nstops = int(
    motion_path_dur_frames / flash_dur_frames)  # num stops along frame's path
motion_x_start = -motion_path_length / 2
motion_x_end = motion_path_length / 2
# create frame's pathway
motion_vector = np.linspace(motion_x_start, motion_x_end, motion_nstops)
# find the index and value of the midway of the frame's path
motion_path_mid_val = motion_vector[int((motion_nstops - 1) / 2)]

probe_radius = .4  # dva
probe_x = 0  # dva from center
probe_y = 0  # dva from center
probe_color_list = ['DodgerBlue', 'Tomato']

replica_radius = .4  # dva
replica_x_org = 10
replica_y_org = 8

anchor_radius = .2  # dva
anchor_color = 'gray'
anchor_positions_base = {
    1: [+frame_half_width, +frame_half_width],   # TR - oben rechts
    2: [-frame_half_width, +frame_half_width],   # TL - oben links
    3: [-frame_half_width, -frame_half_width],   # BL - unten links
    4: [+frame_half_width, -frame_half_width],   # BR - unten rechts
    5: [0,                 +frame_half_width],   # T  - oben Mitte
    6: [-frame_half_width, 0],                   # L  - links Mitte
    7: [0,                 -frame_half_width],   # B  - unten Mitte
    8: [+frame_half_width, 0],                   # R  - rechts Mitte
}

fix_radius = .7  # dva
fix_x = 0  # dva from center
fix_y = 7  # dva from center
fix_dur_sec = 1
fix_dur_frames = int(fix_dur_sec * refresh_rate)

gap_dur_sec = 0.5
gap_dur_frames = int(gap_dur_sec * refresh_rate)

condition_specs = {
    1: ('down',  [1, 2, 7]),
    2: ('right', [2, 3, 8]),
    3: ('up',    [3, 4, 5]),
    4: ('left',  [4, 1, 6]),
}

cnd_array_base = np.array(list(condition_specs.keys()))
nrep_per_trial = 7

# mouse
mouse = event.Mouse(win=win, visible=False)
mouse.setPos([0, 0])
# -------------------------------------------------
# /// VISUAL OBJECTS DEFINITION ///
# -------------------------------------------------
fixdot = visual.TextStim(win=win,
                         text='+',
                         height=fix_radius,
                         color='gray')
probe = visual.Circle(win,
                      radius=probe_radius,
                      pos=[probe_x, probe_y])
anchors = {i: visual.Circle(win,
                            radius=anchor_radius,
                            fillColor=anchor_color,
                            lineColor=None)
           for i in range(1, 9)}
replica1 = visual.Circle(win,
                         radius=replica_radius,
                         fillColor=probe_color_list[0])

replica2 = visual.Circle(win,
                         radius=replica_radius,
                         fillColor=probe_color_list[1])

# -------------------------------------------------
# /// CONDITIONS ///
# -------------------------------------------------
cnd_array = np.repeat(cnd_array_base, nrep_per_trial)
ntrials = nrep_per_trial * len(cnd_array_base)
assert (cnd_array.size == ntrials)
ind_shuffle = np.arange(ntrials)
np.random.shuffle(ind_shuffle)
cnd_array = cnd_array[ind_shuffle]
# -------------------------------------------------
# show the opening message window
# -------------------------------------------------
sup.opening_msg2(win)
# show a blank window for one second
for iframe in range(refresh_rate):
    win.flip()
# #################################################
#                   TRIAL begins
# #################################################
for itrial in range(ntrials):
    # -------------------------------------------------
    # set trial variables
    # -------------------------------------------------
    abortion_flag = False
    confirmation_flag = False
    cnd = int(cnd_array[itrial])
    direction, visible_anchors = condition_specs[cnd]
    replica_x_offset = random.choice([-1, 1])
    replica_x = replica_x_org * replica_x_offset
    replica_y_offset = np.random.rand() * 1
    replica_y = replica_y_org + replica_y_offset
    mouse.setPos([np.random.choice(np.arange(-10, 10+1)), 0])
    # -------------------------------------------------
    # run stimulus
    # -------------------------------------------------
    # run fixation period
    for ifix in range(fix_dur_frames):
        fixdot.pos = fix_x, fix_y
        fixdot.draw()
        win.flip()
    # run gap period
    for igap in range(gap_dur_frames):
        win.flip()
    while not (abortion_flag or confirmation_flag):
        for ileg in range(2):
            # move the frame and flash one probe at the end of its path
            for xind, xval in enumerate(motion_vector[0:-1]):
                for irep in range(flash_dur_frames):

                    # replica
                    [mouse_x, mouse_y] = mouse.getPos()
                    replica_distance = mouse_x
                    replica1.pos = (replica_x + replica_distance / 2,
                                    replica_y)
                    replica2.pos = (replica_x - replica_distance / 2,
                                    replica_y)

                    replica1.draw()
                    replica2.draw()

                    for i in visible_anchors:
                        base = anchor_positions_base[i]
                        anchors[i].pos = (base[0] + xval, base[1])
                        anchors[i].draw()

                    if xind == 0:
                        probe.fillColor = probe_color_list[ileg]
                        probe.draw()

                    [mouse_x, mouse_y] = mouse.getPos()
                    replica_x_offset = mouse_x / 2
                    replica1.pos = (mouse_x, mouse_y)

                    win.flip()

                    # check mouse
                    if mouse.getPressed()[2]:
                        abortion_flag = True
                    if mouse.getPressed()[0]:
                        confirmation_flag = True

            # reverse the frame's path
            motion_vector = motion_vector[::-1]

    if abortion_flag:
        core.quit()

    # run gap period
    for igap in range(gap_dur_frames):
        win.flip()

    # -------------------------------------------------
    # create data frame and save
    # -------------------------------------------------
    # create a dictionary
    trial_dict = {
        'trial_num': [itrial + 1],
        'replica_dist': np.round(mouse_x, 2),
        'cnd': cnd,
        'direction': direction,
    }

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)

    # if first trial create a file, else load and add the new data frame
    if itrial == 0:
        dfnew.to_json(data_path)
    else:
        df = pd.read_json(data_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(data_path)

sup.end_screen(win, 'white')