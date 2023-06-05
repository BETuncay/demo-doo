from typing import Any
import numpy as np


class VBO:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.vbos =  {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['important_cube'] = ImportantCubeVBO(ctx)

    def destroy(self):
        for vbo in self.vbos.values():
            vbo.destroy()
         
class BaseVBO:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.ibo = self.get_ibo()
        self.format = None
        self.attrib = None

    def get_vertex_data(self):
        ... # implemented by subclass

    def get_index_data(self):
        ... # implemented by subclass

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_ibo(self):
        index_data = self.get_index_data()
        ibo = self.ctx.buffer(index_data)
        return ibo

    def destroy(self):
        self.vbo.release()
        self.ibo.release()

class CubeVBO(BaseVBO):
    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.format = '3f'
        self.attrib = ['in_position']

    def get_vertex_data(self):
        return np.array([
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1],

            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
        ], dtype='f4')
    
    def get_index_data(self):
        return np.array([
            [0, 2, 3], [0, 1, 2],
            [1, 7, 2], [1, 6, 7],
            [6, 5, 4], [4, 7, 6],
            [3, 4, 5], [3, 5, 0],
            [3, 7, 4], [3, 2, 7],
            [0, 6, 1], [0, 5, 6]
        ])


class ImportantCubeVBO(BaseVBO):
    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.format = '3f 1f'
        self.attrib = ['in_position', 'in_importance']

    def get_vertex_data(self):
        vertices = np.array([
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1],

            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
        ], dtype='f4')
    
        importance = np.random.rand(8, 1).astype('f4')
        return np.hstack([vertices, importance])

    
    def get_index_data(self):
        return np.array([
            [0, 2, 3], [0, 1, 2],
            [1, 7, 2], [1, 6, 7],
            [6, 5, 4], [4, 7, 6],
            [3, 4, 5], [3, 5, 0],
            [3, 7, 4], [3, 2, 7],
            [0, 6, 1], [0, 5, 6]
        ])