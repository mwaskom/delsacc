from __future__ import division

import numpy as np
import pandas as pd

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

        now = exp.clock.getTime()

        target_x, target_y = flexible_values(exp.p.target_positions)

        info = exp.trial_info(

            wait_iti=flexible_values(exp.p.wait_iti),
            wait_start=flexible_values(exp.p.wait_start),
            wait_cue=flexible_values(exp.p.wait_cue),
            wait_delay=flexible_values(exp.p.wait_delay),

            target_x=target_x,
            target_y=target_y,
            sacc_x=np.nan,
            sacc_y=np.nan,

            onset_trial=np.nan,
            onset_cue=np.nan,
            onset_delay=np.nan,
            onset_response=np.nan,
            onset_feedback=np.nan,
            onset_reset=np.nan,

        )

        estimated_trial_end = (now
                               + info.wait_iti
                               + info.wait_start
                               + info.wait_cue
                               + info.wait_delay
                               + 2)

        if estimated_trial_end > exp.p.run_duration:
            raise StopIteration

        yield info


def run_trial(exp, info):

    # Set up the target for this trial
    pos = info.target_x, info.target_y
    exp.s.target.dot.pos = pos
    exp.p.target_pos = [pos]

    # ~~~ Inter-trial interval
    exp.s.fix.color = exp.p.fix_iti_color
    exp.wait_until(exp.iti_end, draw="fix", iti_duration=info.wait_iti)

    # ~~~ Trial onset
    exp.s.fix.color = exp.p.fix_trial_color
    info.onset_trial = exp.clock.getTime()
    exp.tracker.send_message("Trial {} onset".format(info.trial))
    exp.wait_until(exp.check_abort, info.wait_start, draw="fix")

    # ~~~ Cue period
    info.onset_cue = exp.clock.getTime()
    exp.tracker.send_message("Trial {} cue".format(info.trial))
    exp.wait_until(exp.check_abort, info.wait_cue, draw=["fix", "target"])

    # ~~~ Delay period
    info.onset_delay = exp.clock.getTime()
    exp.tracker.send_message("Trial {} delay".format(info.trial))
    exp.wait_until(exp.check_abort, info.wait_delay, draw="fix")

    # ~~~ Response period
    exp.tracker.send_message("Trial {} response".format(info.trial))
    acq_targ = AcquireTarget(exp, 0)
    res = exp.wait_until(acq_targ,
                         timeout=exp.p.wait_response,
                         draw=None)

    # Handle the response
    if res is None:
        # This means the eye never left the fixation window
        info["result"] = "nochoice"
    elif res["result"] == "nochoice":
        # This means the eye left the fixation window
        # but did not end up in the window corresponding to the target
        res.update(responded=True,
                   result="wrong",
                   correct=False,
                   rt=acq_targ.fix_break_time)
    info.update(pd.Series(res))
    info.onset_response = exp.clock.getTime()

    # Provide feedback
    exp.tracker.send_message("Trial {} feedback".format(info.trial))
    info.onset_feedback = exp.clock.getTime()
    exp.sounds[info.result].play()
    exp.show_feedback("target", info["result"])
    exp.wait_until(exp.check_abort, exp.p.wait_feedback, draw="target")
    exp.s.target.color = exp.p.target_color

    # ~~~ Return to fixation
    exp.tracker.send_message("Trial {} reset".format(info.trial))
    info.onset_reset = exp.clock.getTime()
    exp.wait_until(AcquireFixation(exp), draw="fix")

    return info
