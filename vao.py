from vbo import VBO
from shader import Shader


class VAO:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = Shader(ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            self.program.programs['default'],
            self.vbo.vbos['cube']
        )

        self.vaos['fcube'] = self.get_vao(
            self.program.programs['computeG'],
            self.vbo.vbos['important_cube']
        )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)], vbo.ibo)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()