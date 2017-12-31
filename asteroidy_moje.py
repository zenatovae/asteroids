import pyglet
import math
import random, os
from pyglet import gl

window = pyglet.window.Window(width=900, height=700)

batch = pyglet.graphics.Batch()
objects = []
pressed_keys = set()
ROTATION_SPEED = 200


class SpaceObject:
    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = self.rotation
        self.sprite.draw()

    def delete(self):
        objects.remove(self)
        self.sprite.delete()

    @staticmethod
    def draw_circle(x, y, radius):
        iterations = 20
        s = math.sin(2 * math.pi / iterations)
        c = math.cos(2 * math.pi / iterations)

        dx, dy = radius, 0

        gl.glBegin(gl.GL_LINE_STRIP)
        for i in range(iterations + 1):
            gl.glVertex2f(x + dx, y + dy)
            dx, dy = (dx * c - dy * s), (dy * c + dx * s)
        gl.glEnd()


class Spaceship(SpaceObject):
    def __init__(self):
        self.name = "Spaceship"
        spaceship_image = pyglet.image.load('resources\PNG\playerShip3_blue.png')
        spaceship_image.anchor_x = spaceship_image.width // 2
        spaceship_image.anchor_y = spaceship_image.height // 2
        if spaceship_image.width < spaceship_image.height:
            self.radius = spaceship_image.height // 2
        else:
            self.radius = spaceship_image.width // 2
        self.x = window.width // 2
        self.y = window.height // 2
        self.rotation = 90
        self.x_speed = 0
        self.y_speed = 0
        self.sprite = pyglet.sprite.Sprite(spaceship_image, batch=batch)
        self.acceleration = 0

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

        for obj in objects:
            if obj.name == "Asteroid":
                b = obj
                if self.overlaps(self, b):
                    self.hit_by_spaceship()

    def angle_speed(self, dt):
        angle_radians = math.radians(self.rotation)
        self.x_speed = math.sin(angle_radians) * self.acceleration * dt
        self.y_speed = math.cos(angle_radians) * self.acceleration * dt

    @staticmethod
    def distance(a, b, wrap_size):
        """Distance in one direction (x or y)"""
        result = abs(a - b)
        if result > wrap_size / 2:
            result = wrap_size - result
        return result

    def overlaps(self, a, b):
        """Returns true iff two space objects overlap"""
        distance_squared = (self.distance(a.x, b.x, window.width) ** 2 +
                            self.distance(a.y, b.y, window.height) ** 2)
        max_distance_squared = (a.radius + b.radius) ** 2
        return distance_squared < max_distance_squared

    def hit_by_spaceship(self):
        print("došlo ke srážce")
        self.delete()


class Asteroid(SpaceObject):
    def __init__(self):
        self.name = "Asteroid"
        path = r"resources/PNG/Meteors"
        random_filename = random.choice([
            x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))
        ])
        random_path = "resources/PNG/Meteors/" + random_filename
        asteroid_image = pyglet.image.load(random_path)
        asteroid_image.anchor_x = asteroid_image.width // 2
        asteroid_image.anchor_y = asteroid_image.height // 2
        if asteroid_image.width < asteroid_image.height:
            self.radius = asteroid_image.height // 2
        else:
            self.radius = asteroid_image.width // 2
        print(self.radius)
        self.x = random.uniform(0, window.width)
        self.y = random.uniform(0, window.height)
        self.rotation_on_site = random.randrange(0, 2)
        self.x_speed = random.randrange(-50, 50)
        self.y_speed = random.randrange(-50, 50)
        self.rotation = 0
        self.sprite = pyglet.sprite.Sprite(asteroid_image, batch=batch)

    def tick(self, dt):
        if self.rotation_on_site == 0:
            self.rotation -= ROTATION_SPEED * dt
        if self.rotation_on_site == 1:
            self.rotation += ROTATION_SPEED * dt
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        self.x %= window.width
        self.y %= window.height


spaceship = Spaceship()
objects.append(spaceship)

for i in range(10):
    asteroid = Asteroid()
    objects.append(asteroid)


def draw_all_objects():
    window.clear()
    for obj in objects:
        obj.draw()
        obj.draw_circle(obj.x, obj.y, obj.radius)


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
