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
file_name = f"exp06_{subject}_{date}_{time}.json"
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

frame_half_width = 3

motion_path_length = 6  # dva
motion_path_dur_sec = 0.4
motion_path_dur_frames = int(motion_path_dur_sec * refresh_rate)
motion_nstops = int(motion_path_dur_frames / flash_dur_frames)
motion_x_start = -motion_path_length / 2
motion_x_end = motion_path_length / 2
motion_vector = np.linspace(motion_x_start, motion_x_end, motion_nstops)
motion_path_mid_val = motion_vector[int((motion_nstops - 1) / 2)]

probe_radius = .4  # dva
probe_x = 0
probe_y = 0
probe_color_list = ['DodgerBlue', 'Tomato']

replica_radius = .4
replica_x_org = 10
replica_y_org = 8

anchor_radius = .2
anchor_color = 'gray'

fix_radius = .7
fix_x = 0
fix_y = 5  # dva from center (wie in Exp 1)
fix_dur_sec = 1
fix_dur_frames = int(fix_dur_sec * refresh_rate)

gap_dur_sec = 0.5
gap_dur_frames = int(gap_dur_sec * refresh_rate)

# -------------------------------------------------
# /// CONDITION SPECS ///
# -------------------------------------------------
# 7 y-Positionen mit gleichmäßigem Spacing (1.5 dva):
y_positions = [+5, +4, +3, +2, +1, 0, -1, -2, -3, -4, -5]
y_labels    = [+5, +4, +3, +2, +1, 0, -1, -2, -3, -4, -5]

# condition_specs[cnd] = (label, side, y_pos, n_anchors)
condition_specs = {}
cnd_id = 1
# Conditions 1-7: 2 Anchors (links + rechts)
for y, y_lab in zip(y_positions, y_labels):
    condition_specs[cnd_id] = (f'2anch_{y_lab}', 'both', y, 2)
    cnd_id += 1
# Conditions 8-14: 1 Anchor rechts
for y, y_lab in zip(y_positions, y_labels):
    condition_specs[cnd_id] = (f'1R_{y_lab}', 'right', y, 1)
    cnd_id += 1
# Conditions 15-21: 1 Anchor links
for y, y_lab in zip(y_positions, y_labels):
    condition_specs[cnd_id] = (f'1L_{y_lab}', 'left', y, 1)
    cnd_id += 1

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

anchor_R = visual.Circle(win,
                         radius=anchor_radius,
                         fillColor=anchor_color)
anchor_L = visual.Circle(win,
                         radius=anchor_radius,
                         fillColor=anchor_color)

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
    cnd_label, side, y_pos, n_anch = condition_specs[cnd]

    # Anchor-Basispositionen für diesen Trial (rechte/linke Seite, variable y)
    anchor_R_x0y0 = [+frame_half_width, y_pos]
    anchor_L_x0y0 = [-frame_half_width, y_pos]

    replica_x_offset = random.choice([-1, 1])
    replica_x = replica_x_org * replica_x_offset
    replica_y_offset = np.random.rand() * 1
    replica_y = replica_y_org + replica_y_offset
    mouse.setPos([np.random.choice(np.arange(-10, 10 + 1)), 0])
    # -------------------------------------------------
    # run stimulus
    # -------------------------------------------------
    for ifix in range(fix_dur_frames):
        fixdot.pos = fix_x, fix_y
        fixdot.draw()
        win.flip()

    for igap in range(gap_dur_frames):
        win.flip()

    while not (abortion_flag or confirmation_flag):
        for ileg in range(2):
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

                    # Anchor-Positionen (mit Frame-Bewegung)
                    anchor_R.pos = (anchor_R_x0y0[0] + xval,
                                    anchor_R_x0y0[1])
                    anchor_L.pos = (anchor_L_x0y0[0] + xval,
                                    anchor_L_x0y0[1])

                    # Zeichnen je nach Condition
                    if side in ('both', 'right'):
                        anchor_R.draw()
                    if side in ('both', 'left'):
                        anchor_L.draw()

                    if xind == 0:
                        probe.fillColor = probe_color_list[ileg]
                        probe.draw()

                    [mouse_x, mouse_y] = mouse.getPos()
                    replica_x_offset = mouse_x / 2
                    replica1.pos = (mouse_x, mouse_y)

                    win.flip()

                    if mouse.getPressed()[2]:
                        abortion_flag = True
                    if mouse.getPressed()[0]:
                        confirmation_flag = True

            motion_vector = motion_vector[::-1]

    if abortion_flag:
        core.quit()

    for igap in range(gap_dur_frames):
        win.flip()

    # -------------------------------------------------
    # save trial
    # -------------------------------------------------
    trial_dict = {
        'trial_num': [itrial + 1],
        'replica_dist': np.round(mouse_x, 2),
        'cnd': cnd,
        'cnd_label': cnd_label,
        'side': side,
        'y_pos': y_pos,
        'n_anchors': n_anch,
    }
    dfnew = pd.DataFrame(trial_dict)

    if itrial == 0:
        dfnew.to_json(data_path)
    else:
        df = pd.read_json(data_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(data_path)

sup.end_screen(win, 'white')
