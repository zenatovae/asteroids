import pyglet
spaceship_imp = pyglet.image.load("resources/PNG/playerShip2_red.png")

window = pyglet.window.Window()

class Spaceship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.x_speed = 50
        self.y_speed = 100
        self.shoot_speed = 1/3
        self.sprite = pyglet.sprite.Sprite(spaceship_imp)

    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw()

    def tick(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt

spaceship = Spaceship()

def tick(dt):
    spaceship.tick(dt)

pyglet.clock.schedule_interval(tick, 1/30)

def draw():
    window.clear()
    spaceship.draw()

window.push_handlers(
    on_draw=draw,
)

pyglet.app.run()
