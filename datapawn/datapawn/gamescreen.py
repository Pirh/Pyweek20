from __future__ import print_function, unicode_literals

import pyglet
import pyglet.gl as gl
from pyglet.window import key

from math import fmod

from .entity import Entity, Drawable, Datapawn, SpiritOfTheDrums, Camera, DrawableText
from .music import BeatClock

CONTROLS = {
    key.UP: "D",
    key.DOWN: "0",
    key.LEFT: "-",
    key.RIGHT: "1",
}


class GameScreen(pyglet.window.Window):
    GROUND_Y = 100

    def __init__(self):
        super(GameScreen, self).__init__(800, 450)
        gl.glClearColor(0.5,0.85,1.0,1.0)
        self.batch = pyglet.graphics.Batch()
        self.named_entities = {}
        self.clock = 0.0
        self.frames = 0

        def robot(x):
            return Entity(self, (x, self.GROUND_Y), components=[
                Drawable(image="datapawn.png", batch=self.batch),
                Datapawn()
                ])

        self.entities = [
            Entity(self, (400, 225), components=[Camera()]),
            robot(10),
            robot(40),
            robot(50),
            robot(80),
            Entity(self, (0,0), name="Spirit of the Drums", components=[SpiritOfTheDrums()]),
            Entity(self, (200, 200), name="Ground Text", components=[
                DrawableText(world=True, x=200, y=200, text="This is a test", font_size=80)
            ])
            ]
        for e in self.entities:
            if e.name:
                self.named_entities[e.name] = e

        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)
        self.command = []
        self.beatclock = BeatClock()
        self.beatclock.start()
        self.dispatch_event("on_start")

    def on_key_press(self, symbol, modifiers):
        super(GameScreen, self).on_key_press(symbol, modifiers)
        sym = CONTROLS.get(symbol)
        if sym:
            beat,error = self.beatclock.get_beat()
            status = "Good!"
            if error < -0.12:
                status = "Too Fast"
            elif error > 0.12:
                status = "Too Slow"
            #print("{0}  {1}".format(error, status))
            self.command.append(sym)
            if len(self.command) == 4:
                self.dispatch_event("on_drum_command", ''.join(self.command))
                print(self.command)
                self.command = []

    def tick(self, dt):
        self.clock += dt
        if self.frames % 60 == 0:
            self.clock = self.beatclock.player.time
        self.frames += 1
        self.dispatch_event("on_tick", dt)

    def on_draw(self):
        self.clear()
        self.draw_sky()
        self.draw_ground()
        self.batch.draw()
        self.draw_beat()

    def draw_sky(self):
        skystrip = (
            0, 450,   800, 450,
            0, self.GROUND_Y,   800, self.GROUND_Y
            )
        colors = (0.75,0.8,1.0,0.75,0.8,1.0,0.0,0.33,1.0,0.0,0.33,1.0)
        pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP,
            ("v2f", skystrip), ("c3f", colors))

    def draw_ground(self):
        groundstrip = (
            0, self.GROUND_Y,   800, self.GROUND_Y,
            0, self.GROUND_Y-20,   800, self.GROUND_Y-20,
            0,  0,   800,  0
            )
        colors = (1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0)
        pyglet.graphics.draw(6, pyglet.gl.GL_TRIANGLE_STRIP,
            ("v2f", groundstrip), ("c3f", colors))

    def draw_beat(self):
        blength = self.beatclock.beat_length
        error = fmod(self.clock, blength) / blength
        beat = self.current_beat
        bar = self.current_bar
        playable = self.this_bar_playable

        b = 10 - 8*error
        if not playable:
            b //= 2
        vertices = (
            0, 0,   b, b,   0, 450,   b, 450-b,
            800, 450,   800-b, 450-b,
            800, 0,   800-b, b,   0, 0,   b, b
            )
        if playable:
            colors = (1,1,1)*10
        elif beat == self.beatclock.beats_per_bar - 1 and bar >= 1:
            colors = (1.0,1.0,0.8)*10
        else:
            colors = (0.6,0.6,0.6)*10
        pyglet.graphics.draw(10, pyglet.gl.GL_QUAD_STRIP,
            ("v2f", vertices), ("c3f", colors))

    def end_game(self, message="Victory!"):
        print(message)
        pyglet.app.quit()

    @property
    def current_beat(self):
        return int(self.clock / self.beatclock.bar_length) % self.beatclock.beats_per_bar

    @property
    def current_bar(self):
        return int(self.clock / self.beatclock.bar_length)

    @property
    def this_bar_playable(self):
        bar = self.current_bar
        if bar < 3:
            return False
        return (self.current_bar % 2) == 1

GameScreen.register_event_type("on_tick")
GameScreen.register_event_type("on_start")
GameScreen.register_event_type("on_drum_command")