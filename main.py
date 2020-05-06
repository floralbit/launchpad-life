import time
import launchpad
import conway
import renderer


TIME_STEP_SECONDS = 0.5
TIME_CHANGE_FACTOR = 1.6


if __name__ == '__main__':
    lpad = launchpad.Launchpad()

    past_time = time.time_ns()
    step_timer = 0.0
    playing = True
    lpad.get_pad(launchpad.CONTROL_PAD_FORWARD).set_on(launchpad.COLOR_GREEN) # show we're playing to start

    grid = conway.init_grid()

    print("ready...")
    while True:
        # update dt
        current_time = time.time_ns()
        delta_time = (current_time - past_time) / 1e+9
        past_time = current_time

        if playing:
            step_timer += delta_time

        if step_timer > TIME_STEP_SECONDS:
            step_timer = 0.0
            grid = conway.run_step(grid)
            renderer.draw_grid(lpad, grid)

        events = lpad.poll_events()
        for event in events:
            # print(event)
            if event.event_type == launchpad.EVENT_PRESS:
                if event.pad_type == launchpad.PAD_TYPE_GRID:
                    pad = lpad.get_grid_pad(event.pad_x, event.pad_y)
                    renderer.toggle_pad(pad)
                    grid[event.pad_x][event.pad_y] = not grid[event.pad_x][event.pad_y]

                if event.pad_type == launchpad.PAD_TYPE_CONTROL:
                    pad = lpad.get_pad(event.pad_num)
                    pad.set_on(launchpad.COLOR_PURPLE)

                    if event.pad_num == launchpad.CONTROL_PAD_UP:
                        TIME_STEP_SECONDS = TIME_STEP_SECONDS / TIME_CHANGE_FACTOR
                    if event.pad_num == launchpad.CONTROL_PAD_DOWN:
                        TIME_STEP_SECONDS = TIME_STEP_SECONDS * TIME_CHANGE_FACTOR
                    if event.pad_num == launchpad.CONTROL_PAD_BACK:
                        grid = conway.clear_grid(grid)
                        renderer.draw_grid(lpad, grid)
                    if event.pad_num == launchpad.CONTROL_PAD_FORWARD:
                        playing = not playing
                        if playing:
                            pad.set_on(launchpad.COLOR_GREEN)
                        else:
                            pad.set_on(launchpad.COLOR_RED)
                    if event.pad_num == launchpad.CONTROL_PAD_SESSION:
                        grid = conway.randomize_grid(grid)
                        renderer.draw_grid(lpad, grid)
                    if event.pad_num == launchpad.CONTROL_PAD_VOLUME:
                        step_timer = 0.0
                        grid = conway.run_step(grid)
                        renderer.draw_grid(lpad, grid)
                    if event.pad_num == launchpad.CONTROL_PAD_USER1:
                        renderer.toggle_next_mode()
                        renderer.draw_grid(lpad, grid)
                    if event.pad_num == launchpad.CONTROL_PAD_USER2:
                        conway.toggle_next_game_set()

            if event.event_type == launchpad.EVENT_RELEASE and event.pad_type == launchpad.PAD_TYPE_CONTROL:
                pad = lpad.get_pad(event.pad_num)
                if pad.pad_num != launchpad.CONTROL_PAD_FORWARD: # special case for play/pause
                    pad.set_off()
