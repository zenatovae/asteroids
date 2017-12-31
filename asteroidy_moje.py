import pyglet
import math

spaceship_image = pyglet.image.load('resources\PNG\playerShip3_blue.png')
spaceship_image.anchor_x = spaceship_image.width // 2
spaceship_image.anchor_y = spaceship_image.height // 2

window = pyglet.window.Window(width=800, height=600)

batch = pyglet.graphics.Batch()
objects = []
pressed_keys = set()
ROTATION_SPEED = 200
ACCELERATION = 300


class Spaceship:
    def __init__(self):
        self.x = window.width // 2
        self.y = window.height // 2
        self.rotation = 90
        self.x_speed = 0
        self.y_speed = 0
        self.sprite = pyglet.sprite.Sprite(spaceship_image, batch=batch)
        self.acceleration = 0

    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = self.rotation
        self.sprite.draw()

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation -= ROTATION_SPEED * dt
            if self.rotation < 0:
                self.rotation += 360
            self.angle_speed(dt)
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation += ROTATION_SPEED * dt
            if self.rotation > 360:
                self.rotation -= 360
            self.angle_speed(dt)
        if pyglet.window.key.UP in pressed_keys:
            self.acceleration += 30
            self.angle_speed(dt)
        if pyglet.window.key.DOWN in pressed_keys:
            self.acceleration -= 30
            if self.acceleration < 0:
                self.acceleration = 0
            self.angle_speed(dt)

        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed

        self.x %= window.width
        self.y %= window.height
        # print("rotation is: ", self.rotation)
        # print("x speed is : ", self.x_speed)
        # print("y speed is : ", self.y_speed)
        # print("x is : ", self.x)
        # print("y is : ", self.y)

    def angle_speed(self, dt):
        angle_radians = math.radians(self.rotation)
        self.x_speed = math.sin(angle_radians) * self.acceleration * dt
        self.y_speed = math.cos(angle_radians) * self.acceleration * dt


spaceship = Spaceship()
objects.append(spaceship)


def draw_all_objects():
    window.clear()
    for obj in objects:
        obj.draw()


def tick(dt):
    for obj in objects:
        obj.tick(dt)


pyglet.clock.schedule_interval(tick, 1 / 30)


def key_press(symbol, mod):
    pressed_keys.add(symbol)
    print(pressed_keys)


def key_release(symbol, mod):
    pressed_keys.discard(symbol)
    print(pressed_keys)


window.push_handlers(on_draw=draw_all_objects, on_key_press=key_press, on_key_release=key_release)

pyglet.app.run()
