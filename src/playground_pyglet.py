import pyglet
import pymunk
import pymunk.pyglet_util
from car import PhysicCar
from pymunk import Vec2d
from gui import background_color

if __name__ == "__main__":
    # fps handlings
    fps = 60
    dt = 1 / fps

    # initialization
    window = pyglet.window.Window()
    screen_width = window.width
    screen_height = window.height
    # window.view = window.view.scale((8, 8, 1))
    draw_options = pymunk.pyglet_util.DrawOptions()

    space = pymunk.Space()
    space.gravity = (0, 0)

    # Add objects here
    car = PhysicCar(position=Vec2d(screen_width / 2, screen_height / 2), angle=0)
    car.add(space)

    ### ALL SETUP DONE

    selected = None
    throttle = 0
    wheel_angle = 0
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    def update(dt):
        global throttle, wheel_angle
        r = 1
        for _ in range(r):
            car.update(throttle=throttle, wheel_angle=wheel_angle)
            space.step(dt / r)

    pyglet.clock.schedule_interval(update, dt)
    fps_display = pyglet.window.FPSDisplay(window)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        mouse_body.position = Vec2d(x, y)
        hit = space.point_query(mouse_body.position, 0, pymunk.ShapeFilter())
        if hit != [] and hit[0].shape is not None:
            global selected
            body = hit[0].shape.body
            rest_length = mouse_body.position.get_distance(body.position)
            stiffness = 1000
            damping = 10
            selected = pymunk.DampedSpring(mouse_body, body, (0, 0), (0, 0), rest_length, stiffness, damping)
            space.add(selected)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        global selected
        if selected is not None:
            space.remove(selected)
            selected = None

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        mouse_body.position = x, y

    @window.event
    def on_key_press(symbol, modifiers):
        global throttle, wheel_angle
        match symbol:
            case pyglet.window.key.P:
                pyglet.image.get_buffer_manager().get_color_buffer().save("spiderweb.png")
            case pyglet.window.key.UP:
                throttle += 1.0
            case pyglet.window.key.DOWN:
                throttle -= 1.0
            case pyglet.window.key.LEFT:
                wheel_angle += 1.0
            case pyglet.window.key.RIGHT:
                wheel_angle -= 1.0
            case _:
                pass

    @window.event
    def on_key_release(symbol, modifiers):
        global throttle, wheel_angle
        match symbol:
            case pyglet.window.key.UP:
                throttle -= 1.0
            case pyglet.window.key.DOWN:
                throttle += 1.0
            case pyglet.window.key.LEFT:
                wheel_angle -= 1.0
            case pyglet.window.key.RIGHT:
                wheel_angle += 1.0
            case _:
                pass

    @window.event
    def on_draw():
        window.clear()
        pyglet.gl.glClearColor(*background_color)
        space.debug_draw(draw_options)
        fps_display.draw()

    pyglet.app.run(dt)
