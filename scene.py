from model import *

class Scene:
    def __init__(self, app) -> None:
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        ground_size = 10
        #self.add_object(FCube(self.app, pos=(0, -2, 0), scale=(ground_size, 0.1, ground_size), color=(0.5, 0.5, 0.5, 1)))
        self.add_object(FCube(self.app, pos=(-2.5, 0, 0), scale=(0.5,1,0.5), color=(1, 0, 0, 0.2)))
        self.add_object(FCube(self.app, pos=(0, 0, 0), scale=(0.5,1,0.5), color=(0, 1, 0, 0.2)))
        self.add_object(FCube(self.app, pos=(2.5, 0, 0), scale=(0.5,1,0.5), color=(0, 0, 1, 0.2)))

    def render(self):
        for obj in self.objects:
            obj.render()

    def change_vao(self, vao):
        for obj in self.objects:
            obj.change_vao(vao)