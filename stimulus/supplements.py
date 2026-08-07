from psychopy import monitors, visual, event, core
from datetime import date, datetime


def config_mon_dell():
    monitor = monitors.Monitor('prim_mon', width=52, distance=70)
    monitor.setSizePix([1920, 1080])
    return monitor


def config_win(mon, fullscr):
    win = visual.Window(monitor=mon,
                        units='deg',
                        size=[1920, 1000],
                        pos=[0, 0],
                        fullscr=fullscr,
                        color=[-.8, -.8, -.8])
    win.mouseVisible = True
    return win


def draw_fixdot(win, size, pos):
    fixdot = visual.TextStim(win=win,
                             text='+',
                             height=size,
                             pos=pos,
                             color='white')
    fixdot.draw()


def draw_frame(win, width, pos=(0, 0)):
    if width == 7.5:
        line_width = 0.3
    elif width == 5:
        line_width = 0.2
    else:
        line_width = 0.05
    outer_frame = visual.Rect(win=win,
                              size=width,
                              fillColor='white',
                              pos=pos)
    inner_frame = visual.Rect(win=win,
                              size=width - line_width,
                              fillColor=[-.8, -.8, -.8],
                              pos=pos)
    outer_frame.draw()
    inner_frame.draw()


def draw_probe(win, color, radius=.5, pos=(0, 0), edge_width=0):
    outer_probe = visual.Circle(win,
                                radius=radius + edge_width,
                                fillColor=[-.8, -.8, -.8],
                                pos=pos)
    inner_probe = visual.Circle(win,
                                radius=radius,
                                fillColor=color,
                                pos=pos)
    outer_probe.draw()
    inner_probe.draw()


def get_date():
    today = date.today()
    return (str(today.year).zfill(4) +
            str(today.month).zfill(2) +
            str(today.day).zfill(2))


def get_time():
    now = datetime.now()
    return now.strftime("%H%M%S")


def opening_msg(win):
    text_size = 0.5
    msg = f'In this experiment, your task is to maintain your gaze at ' \
          f'the fixation cross and memorize the location of a single ' \
          f'dot (in red or blue) or two dots (in red and blue) that ' \
          f'flash.\n\n' \
          f'After the mouse cursor appears, you have to click at the ' \
          f'locations you memorized, while maintaining your ' \
          f'fixation.\n\n' \
          f'You can quit the experiment any time by pressing the Escape ' \
          f'button.'

    inst_text = visual.TextStim(win, text=msg, color='white', height=text_size,
                                alignText='left')
    inst_text.pos = (0, 2)
    inst_text.draw()

    commands = '[Escape]: Cancel\t[Space]: OK'
    cmnd_text = visual.TextStim(win, text=commands, color='white', height= text_size,
                                alignText='right')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()
    pressed_key = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in pressed_key:
        core.quit()
    elif 'space' in pressed_key:
        pass


def opening_msg2(win):
    text_size = 0.7
    msg = (
        '1. Maintain your gaze at the fixation cross. \n\n'
        '2. Pay attention to the flashing coloured dots.\n\n'
        '3. How far are the two coloured dots apart?\n\n'
        '4. Use the mouse to replicate the observed distance.\n\n'
        '5. Place each colour on the same side where you saw it.\n\n'
        '6. While adjusting, you may look at the replica.\n\n\n' 
        
        'Left click = start / confirm \n'
        'Right click = quit'
    )

    inst_text = visual.TextStim(
        win=win,
        text=msg,
        color='white',
        height= text_size,
        wrapWidth= 30,
        pos=(8, 0),
        alignText='left'
    )
    #inst_text.pos = (5, 0)

    mouse = event.Mouse(win=win, visible=False)

    while True:

        inst_text.draw()
        win.flip()

        buttons = mouse.getPressed()

        # left mouse button
        if buttons[0]:
            break

        # right mouse button
        if buttons[2]:
            core.quit()

        core.wait(0.01)


def end_screen(win, color='black'):
    msg = 'Experiment finished successfully.\n Thank you!'
    message = visual.TextStim(win,
                              text=msg,
                              color=color,
                              height=.65,
                              alignText='center',
                              pos=(0, 0))
    for i in range(3 * 60):
        message.draw()
        win.flip()
