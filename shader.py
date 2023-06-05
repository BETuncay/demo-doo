class Shader:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.load_shader('default')
        self.programs['computeG'] = self.load_shader('computeG')

    def load_shader(self, file_name):
        with open(f'shaders//{file_name}.vert') as file:
            vert_shader = file.read()
        with open(f'shaders//{file_name}.frag') as file:
            frag_shader = file.read()
        program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        return program

    def destroy(self):
        for program in self.programs.values():
            program.release()