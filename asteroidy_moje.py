import pyglet

spaceship_image = pyglet.image.load('resources\PNG\playerShip3_blue.png')
"""spaceship = pyglet.sprite.Sprite(spaceship_image, x=100, y=150)"""

window = pyglet.window.Window(width=800, height=600)

"""@window.event
def on_draw():
    spaceship.draw()"""


batch = pyglet.graphics.Batch()

spaceship_sprites = []
for i in range(10):
    x, y = i * 70, i * 50
    spaceship_sprites.append(pyglet.sprite.Sprite(spaceship_image, x, y, batch=batch))

@window.event
def on_draw():
    batch.draw()

pyglet.app.run()
