import pyglet

window = pyglet.window.Window()
pressed_keys = set()

spaceship_imp = pyglet.image.load("resources/PNG/playerShip2_red.png")
spaceship_imp.anchor_x = spaceship_imp.width //2
spaceship_imp.anchor_y = spaceship_imp.height //2

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
        self.sprite.rotation = self.rotation
        self.sprite.draw()

    def tick(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation -=4
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation +=4
    #def move

spaceship = Spaceship()

def tick(dt):
    spaceship.tick(dt)

pyglet.clock.schedule_interval(tick, 1/30)

def draw():
    window.clear()
    spaceship.draw()

def key_press(symbol, mod):
    pressed_keys.add(symbol)
    print(pressed_keys)

def key_release(symbol, mod):
    pressed_keys.discard(symbol)
    print(pressed_keys)

window.push_handlers(
    on_draw=draw,
    on_key_press=key_press,
    on_key_release=key_release,
)

pyglet.app.run()
