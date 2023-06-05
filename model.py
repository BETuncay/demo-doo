import moderngl as gl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vao_name, tex_id, color=(1, 0, 0, 1), pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(radius) for radius in rot])
        self.scale = scale
        self.color = color
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self):
        ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        
        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()

    def change_vao(self, vao_name):
        self.vao = self.app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, color=(1, 0, 0, 1), pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
        super().__init__(app, vao_name, tex_id, color, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['color'].value = self.color
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
    
    def on_init(self):
        self.program['color'].value = self.color
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)


class FCube(BaseModel):
    def __init__(self, app, vao_name='fcube', tex_id=0, color=(1, 0, 0, 1), pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
        super().__init__(app, vao_name, tex_id, color, pos, rot, scale)
        self.on_init()

    def update(self):
        #self.texture.use()
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        self.program['camera_pos'].write(self.camera.position)
    
    def on_init(self):
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        self.program['camera_pos'].write(self.camera.position)