
base = dict(

    display_name="macbook-air",
    display_luminance=35,

    monitor_eye=True,
    eye_fixation=True,
    eye_response=True,

    fix_iti_color=(-.9, -.9, -.9),

    target_color=(.8, .6, -.8),
    target_radius=.25,
    target_window=1.5,

    target_positions=[(10, 5), (10, -5), (-10, -5), (-10, 5)],

    wait_iti=2,
    wait_start=("truncexpon", .5, .5, 1),
    wait_cue=.2,
    wait_delay=[4, 8, 12],
    wait_response=2,
    wait_feedback=1,

    run_duration=540,

    perform_acc_target=.8,

)

scan = base.copy()
scan.update(

    display_name="nyu-cbi-propixx",

    trigger=["5"],

    wait_iti=("truncexpon", 2, 6, 3),

)
