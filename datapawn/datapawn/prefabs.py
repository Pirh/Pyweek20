from .entity import *
from .collision import *
from .constants import MASK

def robot(window, x, y, batch):
    return Entity(window, (x, window.GROUND_Y), components=[
        Drawable(image="datapawn.png", batch=batch),
        RectCollider(24, 64, layermask=MASK["robot"]),
        Datapawn()
        ])

def scenery(window, x, y, batch, image, layer=6, parallax=1.0, loop=None):
    d = Drawable(image=image, batch=batch, layer=layer,
                 parallax=parallax, loop=loop)
    return Entity(window, (x, y), components=[d])

def button(window, x, y, batch, image, key):
    return Entity(window, (x, y), components=[
        Drawable(image=image, batch=batch, layer=10, parallax=0.0),
        DrumButton(key)
        ])

def obstacle(window, x, y, batch, image, width, height, layer=7, hp=4, victory=False):
    return Entity(window, (x, y), components=[
        Drawable(image=image, batch=batch, layer=layer),
        RectCollider(width, height, layermask=MASK["obstacle"]),
        Obstacle(hp, {"hit": "hit.wav", "die": "crumble.wav"}, victory=victory)])


def ground_text(window, x, batch, text, font_scale=0.8, font_name="Courier"):
    y = window.GROUND_Y * 0.5
    d = DrawableText(text=text, x=x, world=True, font_name=font_name,
                     font_size=window.GROUND_Y * font_scale,
                     y=y, batch=batch,
                     anchor_x='center', anchor_y='center')
    return Entity(window, (x, y), components=[d])

def sky_text(window, x, y, batch, text, font_size, font_name="Courier"):
    d = DrawableText(text=text, x=x, y=y, world=False, font_name=font_name,
                     font_size=font_size, batch=batch, anchor_x='center', anchor_y='center')
    return Entity(window, (x, y), components=[d])

def moonlight(window, x, y, batch):
    return Entity(window, (x, y), components=[
        Drawable("moonlight.png", batch, layer=9),
        Moonlight()
        ])
