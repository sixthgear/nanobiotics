"""
Please forgive me.
"""

import pyglet

pyglet.resource.path = ['data']
pyglet.resource.reindex()

pyglet.resource.add_font('REZ.ttf')
pyglet.font.load('REZ')

spritesheet = pyglet.image.ImageGrid(pyglet.resource.image('sprites.png'),16,16).get_texture_sequence()
for sprite in spritesheet:
    sprite.anchor_x = sprite.width / 2 
    sprite.anchor_y = sprite.height / 2 

background = pyglet.resource.image('stage_1_background.png')