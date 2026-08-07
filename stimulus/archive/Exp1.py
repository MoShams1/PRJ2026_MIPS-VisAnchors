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
subject = 'test'
# -------------------------------------------------
# destination file
# -------------------------------------------------
date = sup.get_date()
time = sup.get_time()
file_name = f"exp01_{subject}_{date}_{time}.json"
data_path = os.path.join('..', 'data', file_name)
# -------------------------------------------------
# initialize display
# -------------------------------------------------
monitor = monitors.Monitor('prim_mon', width=52, distance=70)
monitor.setSizePix([1920, 1080])
win = visual.Window(monitor=monitor,
                    units='deg',
                    size=[1920, 1000],
                    pos=[0, 0],
                    fullscr=True,
                    color='black')
win.mouseVisible = True
refresh_rate = 120
# -------------------------------------------------
# set up task parameters
# -------------------------------------------------
flash_dur_frames = 2  # frames

frame_half_width = 3

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

replica_x_org = 10
replica_y_org = 8

anchor_radius = .2  # dva
anchor_color = 'gray'
anchor1_x0y0=[+frame_half_width, +frame_half_width]
anchor2_x0y0=[-frame_half_width, +frame_half_width]
anchor3_x0y0=[-frame_half_width, -frame_half_width]
anchor4_x0y0=[+frame_half_width, -frame_half_width]

fix_radius = .7  # dva
fix_x = 0  # dva from center
fix_y = 8  # dva from center
fix_dur_sec = 1
fix_dur_frames = int(fix_dur_sec * refresh_rate)

gap_dur_sec = 0.5
gap_dur_frames = int(gap_dur_sec * refresh_rate)

visanchor_cnd_array_base = np.arange(1, 12)
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
anchor1 = visual.Circle(win,
                        radius=anchor_radius,
                        fillColor=anchor_color)

anchor2 = visual.Circle(win,
                        radius=anchor_radius,
                        fillColor=anchor_color)
anchor3 = visual.Circle(win,
                        radius=anchor_radius,
                        fillColor=anchor_color)
anchor4 = visual.Circle(win,
                        radius=anchor_radius,
                        fillColor=anchor_color)
replica1 = visual.Circle(win,
                         radius=probe_radius,
                         fillColor=probe_color_list[0])

replica2 = visual.Circle(win,
                         radius=probe_radius,
                         fillColor=probe_color_list[1])
# -------------------------------------------------
# /// CONDITIONS ///
# -------------------------------------------------
visanchor_cnd_array = np.repeat(visanchor_cnd_array_base, nrep_per_trial)
ntrials = nrep_per_trial * len(visanchor_cnd_array_base)
# create an equal number of trials per condition
assert (visanchor_cnd_array.size == ntrials)
# randomize the order of each condition array
ind_shuffle = np.arange(ntrials)
np.random.shuffle(ind_shuffle)
visanchor_cnd_array = visanchor_cnd_array[ind_shuffle]
# -------------------------------------------------
# show the opening message window
# -------------------------------------------------
sup.opening_msg(win)
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
    visanchor_cnd = visanchor_cnd_array[itrial]
    mouse.setPos = ([500, 500])
    replica_x_offset = random.choice([-1, 1])
    replica_x = replica_x_org * replica_x_offset
    replica_y_offset = np.random.rand() * 1
    replica_y = replica_y_org + replica_y_offset
    # -------------------------------------------------
    # run stimulus
    # -------------------------------------------------
    # run fixation period
    for ifix in range(fix_dur_frames):
        fixdot.pos = replica_x, replica_y
        fixdot.draw()
        win.flip()
    # run gap period
    for igap in range(gap_dur_frames):
        win.flip()
    while True:
        for ileg in range(2):
            # move the frame and flash one probe at the end of its path
            for xind, xval in enumerate(motion_vector[0:-1]):
                for irep in range(flash_dur_frames):

                    # replica
                    [mouse_x, mouse_y] = mouse.getPos()
                    replica_distance = mouse_x
                    replica1.pos = (replica_x + replica_distance / 2,
                                    replica_y)
                    replica1.draw()
                    replica2.pos = (replica_x - replica_distance / 2,
                                    replica_y)
                    replica2.draw()

                    anchor1.pos = anchor1_x0y0[0] + xval, anchor1_x0y0[1]
                    anchor2.pos = anchor2_x0y0[0] + xval, anchor2_x0y0[1]
                    anchor3.pos = anchor3_x0y0[0] + xval, anchor3_x0y0[1]
                    anchor4.pos = anchor4_x0y0[0] + xval, anchor4_x0y0[1]

                    if visanchor_cnd in [1, 5, 8, 9, 11]:
                        anchor1.draw()
                    if visanchor_cnd in [2, 5, 6, 10, 11]:
                        anchor2.draw()
                    if visanchor_cnd in [3, 6, 7, 9, 11]:
                        anchor3.draw()
                    if visanchor_cnd in [4, 7, 8, 10, 11]:
                        anchor4.draw()

                    if xind == 0:
                        probe.fillColor = probe_color_list[ileg]
                        probe.draw()

                    [mouse_x, mouse_y] = mouse.getPos()
                    replica_x_offset = mouse_x / 2
                    replica1.pos = (mouse_x, mouse_y)

                    win.flip()

            # reverse the frame's path
            motion_vector = motion_vector[::-1]

        # exit when escape button pressed
        pressed_keys = event.getKeys(keyList=['escape', 'space'])
        if 'escape' in pressed_keys:
            core.quit()
        if 'space' in pressed_keys:
            break

    # run gap period
    for igap in range(gap_dur_frames):
        win.flip()

    # -------------------------------------------------
    # create data frame and save
    # -------------------------------------------------
    # create a dictionary
    trial_dict = {'trial_num': [itrial + 1],
                  'replica_dist': mouse_x,
                  'visanchor_cnd': visanchor_cnd}

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