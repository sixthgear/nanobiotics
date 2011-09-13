"""
Please forgive me.
"""

import pyglet

pyglet.resource.path = ['data']
pyglet.resource.reindex()

pyglet.resource.add_font('DYLOVASTUFF.ttf')
pyglet.font.load('DYLOVASTUFF')

spritesheet = pyglet.image.ImageGrid(pyglet.resource.image('sprites.png'),8,8).get_texture_sequence()
for sprite in spritesheet:
    sprite.anchor_x = sprite.width // 2 
    sprite.anchor_y = sprite.height // 2 

bullet = pyglet.resource.image('bullet.png')
bullet.anchor_x = bullet.width // 2
bullet.anchor_y = bullet.height // 2

background = pyglet.resource.image('stage_1_background.png')

cursor = spritesheet[7]