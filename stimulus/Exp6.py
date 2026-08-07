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

# Default frame_half_width (Referenzwert; wird in horizontalen Conditions variiert)
frame_half_width_default = 3

motion_path_length = 6  # dva
motion_path_dur_sec = 0.4
motion_path_dur_frames = int(motion_path_dur_sec * refresh_rate)
motion_nstops = int(motion_path_dur_frames / flash_dur_frames)
motion_x_start = -motion_path_length / 2
motion_x_end = motion_path_length / 2
motion_vector = np.linspace(motion_x_start, motion_x_end, motion_nstops)
motion_path_mid_val = motion_vector[int((motion_nstops - 1) / 2)]

probe_radius = .4
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
fix_y = 7
fix_dur_sec = 1
fix_dur_frames = int(fix_dur_sec * refresh_rate)

gap_dur_sec = 0.5
gap_dur_frames = int(gap_dur_sec * refresh_rate)

# -------------------------------------------------
# /// CONDITION SPECS ///
# -------------------------------------------------
y_fixed = 3  # dva (top-Anchors)

# condition_specs[cnd] = (label, manipulation, frame_half_width, y_top, y_bottom)
condition_specs = {
    # Vertikal: top fix bei y=3, bottom progressiv weiter runter
    1:  ('vert_bottom_0',  'vertical',   frame_half_width_default, y_fixed, 0),
    2:  ('vert_bottom_1.5',    'vertical',   frame_half_width_default, y_fixed, 1.5),
    3:  ('vert_bottom_3',  'vertical',   frame_half_width_default, y_fixed, 3),
    4:  ('vert_bottom_6',    'vertical',   frame_half_width_default, y_fixed, 6),
    5:  ('vert_bottom_9', 'vertical',   frame_half_width_default, y_fixed, 9),
    # Horizontal: alle 4 Anchors bei y=±3, frame_half_width variiert
    6:  ('horiz_width_1',    'horizontal', 1, y_fixed, y_fixed),
    7:  ('horiz_width_2',    'horizontal', 2, y_fixed, y_fixed),
    8:  ('horiz_width_3',    'horizontal', 3, y_fixed, y_fixed),  # normal
    9:  ('horiz_width_4',    'horizontal', 4, y_fixed, y_fixed),
    10: ('horiz_width_5',    'horizontal', 5, y_fixed, y_fixed),
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
anchor1 = visual.Circle(win, radius=anchor_radius, fillColor=anchor_color)
anchor2 = visual.Circle(win, radius=anchor_radius, fillColor=anchor_color)
anchor3 = visual.Circle(win, radius=anchor_radius, fillColor=anchor_color)
anchor4 = visual.Circle(win, radius=anchor_radius, fillColor=anchor_color)
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
    abortion_flag = False
    confirmation_flag = False
    cnd = int(cnd_array[itrial])
    cnd_label, manipulation, fhw, y_top, y_bottom = condition_specs[cnd]

    # Anchor-Basispositionen für diesen Trial
    anchor1_x0y0 = [+fhw, +y_top]    # upper right
    anchor2_x0y0 = [-fhw, +y_top]    # upper left
    anchor3_x0y0 = [-fhw, -y_bottom] # lower left
    anchor4_x0y0 = [+fhw, -y_bottom] # lower right

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

                    anchor1.pos = anchor1_x0y0[0] + xval, anchor1_x0y0[1]
                    anchor2.pos = anchor2_x0y0[0] + xval, anchor2_x0y0[1]
                    anchor3.pos = anchor3_x0y0[0] + xval, anchor3_x0y0[1]
                    anchor4.pos = anchor4_x0y0[0] + xval, anchor4_x0y0[1]

                    anchor1.draw()
                    anchor2.draw()
                    anchor3.draw()
                    anchor4.draw()

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
        'manipulation': manipulation,
        'frame_half_width': fhw,
        'y_top': y_top,
        'y_bottom': y_bottom,
    }
    dfnew = pd.DataFrame(trial_dict)

    if itrial == 0:
        dfnew.to_json(data_path)
    else:
        df = pd.read_json(data_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(data_path)

sup.end_screen(win, 'white')
