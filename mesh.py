from vao import VAO
#from texture import Texture


class Mesh:
    def __init__(self, app) -> None:
        self.app = app
        self.vao = VAO(app.ctx)
        #self.texture = Texture

    def destroy(self):
        self.vao.destroy()
