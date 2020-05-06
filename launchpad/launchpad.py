import pygame
import pygame.midi
import random
from .colors import *
from .pad_nums import *

GRID_WIDTH = 8
GRID_HEIGHT = 8

EVENT_PRESS = 'EVENT_PRESS'
EVENT_RELEASE = 'EVENT_RELEASE'

PAD_TYPE_GRID = 'PAD_TYPE_GRID'
PAD_TYPE_CONTROL = 'PAD_TYPE_CONTROL'


class Launchpad:
    def __init__(self):
        pygame.init()
        pygame.midi.init()

        self.midi_input = pygame.midi.Input(pygame.midi.get_default_input_id())
        self.midi_output = pygame.midi.Output(pygame.midi.get_default_output_id())

        self.pads = {}
        for x in range(0, GRID_WIDTH):
            for y in range(0, GRID_HEIGHT):
                pad_num = Launchpad.grid_x_y_to_pad_number(x, y)
                self.pads[pad_num] = Pad(self.midi_output, pad_num)

        for pad_num in CONTROL_PADS:
            self.pads[pad_num] = Pad(self.midi_output, pad_num)

    def poll_events(self):
        launchpad_events = []

        if self.midi_input.poll():
            data = self.midi_input.read(1000)
            events = pygame.midi.midis2events(data, pygame.midi.get_default_input_id())
            for event in events:
                note_number = event.data1
                velocity = event.data2
                event_type = EVENT_PRESS
                pad_type = PAD_TYPE_GRID

                if velocity == 0:
                    event_type = EVENT_RELEASE

                grid_x, grid_y = Launchpad.pad_number_to_grid_x_y(note_number)
                if grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT: # out of grid, control
                    pad_type = PAD_TYPE_CONTROL

                launchpad_events.append(PadEvent(event_type, pad_type, pad_num=note_number, pad_x=grid_x, pad_y=grid_y))

        return launchpad_events

    def get_grid_pad(self, grid_x, grid_y):
        pad_num = Launchpad.grid_x_y_to_pad_number(grid_x, grid_y)
        return self.pads[pad_num]

    def get_pad(self, pad_num):
        return self.pads[pad_num]

    @staticmethod
    def pad_number_to_grid_x_y(pad_number):
        grid_x = (pad_number % 10) - 1
        grid_y = (pad_number // 10) - 1
        return grid_x, grid_y

    @staticmethod
    def grid_x_y_to_pad_number(x, y):
        return int(f"{y+1}{x+1}")


class PadEvent:
    def __init__(self, event_type, pad_type, pad_x=0, pad_y=0, pad_num=0):
        self.event_type = event_type
        self.pad_type = pad_type
        if pad_type == PAD_TYPE_GRID:
            self.pad_x = pad_x
            self.pad_y = pad_y
        else:
            self.pad_num = pad_num

    def __repr__(self):
        if self.pad_type == PAD_TYPE_CONTROL:
            return f"<{self.event_type} {self.pad_type} {self.pad_num}>"
        return f"<{self.event_type} {self.pad_type} {self.pad_x} {self.pad_y}>"


class Pad:
    def __init__(self, midi_output, pad_num):
        self.midi_output = midi_output
        self.pad_num = pad_num

        self.toggled = False
        self.write(COLOR_OFF)

    def write(self, color=COLOR_OFF):
        status = 176 if self.pad_num in ALT_STATUS_PADS else 144
        self.midi_output.write([[[status, self.pad_num, color, 0], 0]])

    def toggle(self, color=None):
        if self.toggled:
            self.set_off()
        else:
            self.set_on(color=color)

    def set_on(self, color=None):
        if not color:
            self.write(random.choice(COLORS))
        else:
            self.write(color)
        self.toggled = True

    def set_off(self):
        self.write(COLOR_OFF)
        self.toggled = False
