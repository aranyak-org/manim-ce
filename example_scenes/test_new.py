import time

import pyglet
from PIL import Image
from pyglet import shapes
from pyglet.gl import Config
from pyglet.window import Window
import numpy as np
import manim.utils.color.manim_colors as col
from manim._config import tempconfig
from manim.camera.camera import OpenGLCamera, OpenGLCameraFrame
from manim.constants import OUT, RIGHT, UP
from manim.mobject.geometry.arc import Circle
from manim.mobject.geometry.polygram import Square
from manim.mobject.logo import ManimBanner
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
from manim.renderer.opengl_renderer import OpenGLRenderer
from manim._config import config

if __name__ == "__main__":
    with tempconfig({"renderer": "opengl"}):
        renderer = OpenGLRenderer(1920, 1080, background_color=col.GRAY)
        # vm = OpenGLVMobject([col.RED, col.GREEN])
        vm = Circle(
            radius=1, stroke_color=col.YELLOW, fill_opacity=1, fill_color=col.RED
        ).shift(RIGHT)
        vm2 = Square(stroke_color=col.GREEN, fill_opacity=0, stroke_opacity=1).move_to((0,0,-0.5))
        vm3 = ManimBanner()
        # vm.set_points_as_corners([[-1920/2, 0, 0], [1920/2, 0, 0], [0, 1080/2, 0]])
        # print(vm.color)
        # print(vm.fill_color)
        # print(vm.stroke_color)

        camera = OpenGLCameraFrame()
        camera.save_state()
        renderer.init_camera(camera)

        # renderer.render(camera, [vm, vm2])
        # image = renderer.get_pixels()
        # print(image.shape)
        # Image.fromarray(image, "RGBA").show()
        # exit(0)
        win = Window(
            width=1920,
            height=1080,
            vsync=True,
            config=Config(double_buffer=True, samples=4),
        )
        renderer.use_window()

        vm.apply_depth_test()
        vm2.apply_depth_test()
        vm3.apply_depth_test()
        clock = pyglet.clock.get_default()
        def update_circle(dt):
            vm.move_to((np.sin(dt), np.cos(dt), -1))
        clock.schedule(update_circle)

        def p2m(x,y,z):
            from manim._config import config
            return (config.frame_width*(x/config.pixel_width-0.5), config.frame_height*(y/config.pixel_height-0.5),z)


        @win.event
        def on_close():
            win.close()

        @win.event
        def on_mouse_motion(x, y, dx, dy):
            # vm.move_to((14.2222 * (x / 1920 - 0.5), 8 * (y / 1080 - 0.5), 0))
            #camera.move_to(p2m(x,y,camera.get_center()[2]))
            from scipy.spatial.transform import Rotation
            camera.set_orientation(Rotation.from_rotvec((-UP*(x/1920-0.5)+RIGHT*(y/1080-0.5))*2*3.1415))
            # vm.set_color(col.RED.interpolate(col.GREEN,x/1920))
            # print(x,y)

        @win.event
        def on_draw():
            renderer.render(camera, [vm, vm2, vm3])
            pass

        @win.event
        def on_resize(width, height):
            pass

        while True:
            pyglet.clock.tick()
            pyglet.app.platform_event_loop.step()
            win.switch_to()
            win.dispatch_event("on_draw")
            win.dispatch_events()
            win.flip()
