import moderngl as gl
import pygame as pg
import numpy as np
import sys
from camera import Camera
from mesh import Mesh
from scene import Scene
import imgui
from imgui.integrations.pygame import PygameRenderer
import cv2
import matplotlib.pyplot as plt


# soll ich fourier für jeden pixel berechnen oder für jeden vertex und dann interpolieren? -> jeden pixel einfach
class GraphicsEngine:
    def __init__(self, window_size=(1600, 900)) -> None:
        # pygame
        pg.init()
        self.WINDOW_SIZE = window_size
        pg.display.set_mode(self.WINDOW_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # dearimgui
        #imgui.create_context()
        #self.impl = PygameRenderer()
        #io = imgui.get_io()
        #io.display_size = window_size

        # moderngl
        self.ctx = gl.create_context()
        #self.ctx.enable(flags=gl.DEPTH_TEST | gl.CULL_FACE | gl.BLEND)
        self.ctx.enable(flags=gl.BLEND)
        #self.ctx.blend_func = gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA
        self.ctx.blend_func = gl.ADDITIVE_BLENDING
        self.clock = pg.time.Clock()
        self.camera = Camera(self)
        self.time = 0
        self.delta_time = 0
        self.mesh = Mesh(self)
        self.scene = Scene(self)

        self.a_k1 = self.ctx.texture(self.WINDOW_SIZE, 1, dtype='f4')
        self.a_k2 = self.ctx.texture(self.WINDOW_SIZE, 1, dtype='f4')
        self.b_k1 = self.ctx.texture(self.WINDOW_SIZE, 1, dtype='f4')
        self.b_k2 = self.ctx.texture(self.WINDOW_SIZE, 1, dtype='f4')
        self.fbo = self.ctx.framebuffer(color_attachments=[self.a_k1, self.a_k2, self.b_k1, self.b_k2])
        
    def opacity_fourier_render(self):
        # fourier opacity
        self.fbo.use()
        self.fbo.clear(color=(0.0, 0.0, 0.0))
        self.scene.render()

        # nächster render -> framebuffer als uniform input
        #a_k1_array = np.frombuffer(self.fbo.read(attachment=0, components=1, dtype='f4'), dtype=np.float32).reshape(self.fbo.height, self.fbo.width, -1)
        #im = plt.imshow(a_k1_array, cmap=plt.cm.gray)
        #plt.colorbar(im)
        #plt.show()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        self.opacity_fourier_render()

        self.ctx.screen.use()
        self.ctx.clear(color=(0.2, 0.2, 0.2))
        self.scene.render()
        pg.display.flip()

       
    def run(self):
        while True:
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(90)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()