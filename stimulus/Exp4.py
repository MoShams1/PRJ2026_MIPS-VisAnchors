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
file_name = f"exp07_{subject}_{date}_{time}.json"
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

# Frame-Referenzwerte (für Null-Conditions und die orthogonale Achse)
frame_default = 3  # dva — Halbe Frame-Größe im Normalzustand

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
# condition_specs[cnd] = (label, manipulation, abstand, n_anchors)
condition_specs = {
    # Vertikale Conditions: top und bottom Anchors bei y = ±Abstand
    # Bei Abstand=0 (Null): nur 2 obere Anchors bei (±3, +3)
    1: ('v_abstand_0',   'vertical',   0.0, 2),
    2: ('v_abstand_0.75', 'vertical', 0.75, 4),
    3: ('v_abstand_1.5', 'vertical',   1.5, 4),
    4: ('v_abstand_3',   'vertical',   3.0, 4),
    5: ('v_abstand_4.5', 'vertical',   4.5, 4),
    # Horizontale Conditions: left und right Anchors bei x = ±Abstand
    # Bei Abstand=0 (Null): nur 2 mittlere Anchors bei (0, ±3)
    6: ('h_abstand_0',   'horizontal', 0.0, 2),
    7: ('v_abstand_0.75', 'vertical', 0.75, 4),
    8: ('h_abstand_1.5', 'horizontal', 1.5, 4),
    9: ('h_abstand_3',   'horizontal', 3.0, 4),
    10: ('h_abstand_4.5', 'horizontal', 4.5, 4),
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
    cnd_label, manipulation, abstand, n_anch = condition_specs[cnd]

    # ----- Anchor-Basispositionen pro Condition -----
    if manipulation == 'vertical':
        if abstand == 0:
            # Null-Condition: nur 2 obere Anchors bei (±3, +3)
            anchor1_x0y0 = [+frame_default, +frame_default]  # top right
            anchor2_x0y0 = [-frame_default, +frame_default]  # top left
            anchor3_x0y0 = None
            anchor4_x0y0 = None
        else:
            # 4 Anchors symmetrisch um y=0, x bei ±3
            anchor1_x0y0 = [+frame_default, +abstand]  # upper right
            anchor2_x0y0 = [-frame_default, +abstand]  # upper left
            anchor3_x0y0 = [-frame_default, -abstand]  # lower left
            anchor4_x0y0 = [+frame_default, -abstand]  # lower right
    else:  # horizontal
        if abstand == 0:
            # Null-Condition: 2 Anchors in der Mitte des Frames bei (0, ±3)
            anchor1_x0y0 = [0, +frame_default]  # top middle
            anchor2_x0y0 = [0, -frame_default]  # bottom middle
            anchor3_x0y0 = None
            anchor4_x0y0 = None
        else:
            # 4 Anchors symmetrisch um x=0, y bei ±3
            anchor1_x0y0 = [+abstand, +frame_default]  # upper right
            anchor2_x0y0 = [-abstand, +frame_default]  # upper left
            anchor3_x0y0 = [-abstand, -frame_default]  # lower left
            anchor4_x0y0 = [+abstand, -frame_default]  # lower right

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

                    # Anchor 1 & 2 immer zeichnen
                    anchor1.pos = anchor1_x0y0[0] + xval, anchor1_x0y0[1]
                    anchor2.pos = anchor2_x0y0[0] + xval, anchor2_x0y0[1]
                    anchor1.draw()
                    anchor2.draw()

                    # Anchor 3 & 4 nur bei n_anch == 4
                    if n_anch == 4:
                        anchor3.pos = anchor3_x0y0[0] + xval, anchor3_x0y0[1]
                        anchor4.pos = anchor4_x0y0[0] + xval, anchor4_x0y0[1]
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
        'abstand': abstand,
        'n_anchors': n_anch,
        'frame_length': abstand * 2,  # absolute Frame-Länge in Manipulation-Richtung
    }
    dfnew = pd.DataFrame(trial_dict)

    if itrial == 0:
        dfnew.to_json(data_path)
    else:
        df = pd.read_json(data_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(data_path)

sup.end_screen(win, 'white')
