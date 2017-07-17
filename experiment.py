from __future__ import division
import json

import numpy as np
import pandas as pd

from psychopy import core, visual
from visigoth import AcquireFixation, AcquireTarget, flexible_values
from visigoth.stimuli import Point

def create_stimuli(exp):
    """Define stimulus objects."""
    # Fixation point
    fix = Point(exp.win,
                exp.p.fix_pos,
                exp.p.fix_radius,
                exp.p.fix_color)

    target = Point(exp.win,
                   exp.p.fix_pos,
                   exp.p.target_radius,
                   exp.p.target_color)

    return locals()


def generate_trials(exp):

    for t in exp.trial_count():

        target_x, target_y = flexible_values(exp.p.target_positions)

        wait_iti = flexible_values(exp.p.wait_iti)
        wait_delay = flexible_values(exp.p.wait_delay)

        info = exp.trial_info(

            wait_iti=wait_iti,
            wait_cue=exp.p.wait_cue,
            wait_delay=wait_delay,
            target_x=target_x,
            target_y=target_y,

        )

        yield info


def run_trial(exp, info):

    pos = info.target_x, info.target_y
    exp.s.target.dot.pos = pos
    exp.p.target_pos = [pos]

    exp.s.fix.color = exp.p.fix_iti_color
    exp.wait_until(exp.iti_end, draw="fix", iti_duration=info.wait_iti)

    # ~~~ Trial onset
    exp.s.fix.color = exp.p.fix_trial_color

    res = exp.wait_until(AcquireFixation(exp),
                         timeout=exp.p.wait_fix,
                         draw="fix")

    if res is None:
        info["result"] = "nofix"
        exp.sounds.nofix.play()
        return info

    # ~~~ Cue period
    exp.wait_until(timeout=exp.p.wait_cue, draw=["fix", "target"])

    # ~~~ Delay period
    exp.wait_until(timeout=info.wait_delay, draw=["fix"])

    # ~~~ Response period
    acq_targ = AcquireTarget(exp, 0)
    res = exp.wait_until(acq_targ,
                         timeout=exp.p.wait_response,
                         draw=None)

    if res is None:
        # This means the eye never left the fixation window
        info["result"] = "nochoice"
    elif res["result"] == "nochoice":
        # This means the eye left the fixation window
        # but did not end up in the window corresponding to the target
        res.update(responded=True,
                   result="wrong",
                   rt=acq_targ.fix_break_time)

    info.update(pd.Series(res))
    exp.sounds[info.result].play()
    exp.show_feedback("target", info["result"])
    exp.wait_until(timeout=exp.p.wait_feedback, draw="target")
    exp.s.target.color = exp.p.target_color
