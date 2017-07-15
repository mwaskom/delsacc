
base = dict(

    display_name="macbook-air",
    display_luminance=35,

    monitor_eye=True,
    eye_response=True,

    fix_iti_color=(-.9, -.9, -.9),

    target_color=1,
    target_radius=.3,
    target_window=1,

    target_positions=[(10, 5), (10, -5), (-10, -5), (-10, 5)],

    wait_iti=2,
    wait_cue=.5,
    wait_delay=[2, 4],
    wait_response=2,
    wait_feedback=1,

    run_duration=540,

)

scan = base.copy()
scan.update(

    display_name="nyu-cbi-propixx",
    trigger=["5"],

    wait_pre_run=0,

)
