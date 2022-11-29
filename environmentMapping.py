from BaseModel import BaseModel,DrawModelFromMesh
from mesh import *

from OpenGL.GL.framebufferobjects import *

from cubeMap import CubeMap, PlaneMap

from shaders import *

from framebuffer import Framebuffer


class EnvironmentShader(BaseShaderProgram):
    def __init__(self, name='environment', map=None):
        BaseShaderProgram.__init__(self, name=name)
        self.add_uniform('VM')
        self.add_uniform('VMiT')
        self.add_uniform('VT')
        self.add_uniform('plane')
        self.map = map

    def bind(self, model, M, plane=np.array([0, -1, 0, 10000], 'f')):
        if self.map is not None:
            #self.map.update(model.scene)
            unit = len(model.mesh.textures)
            self.uniforms['textureObject'].bind(0)
            self.uniforms['has_texture'].bind(1)
            glActiveTexture(GL_TEXTURE0)
            self.map.bind()
            # self.uniforms['sampler_cube'].bind(0)

        glUseProgram(self.program)

        P = model.scene.P  # get projection matrix from the scene
        V = model.scene.camera.V  # get view matrix from the camera

        # set the PVM matrix uniform
        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))

        # set the PVM matrix uniform
        self.uniforms['VM'].bind(np.matmul(V, M))

        # set the PVM matrix uniform
        self.uniforms['VMiT'].bind(np.linalg.inv(np.matmul(V, M))[:3, :3].transpose())

        self.uniforms['VT'].bind(V.transpose()[:3, :3])


class EnvironmentMappingTexture(PlaneMap):
    def __init__(self, width=200, height=200):
        CubeMap.__init__(self)

        self.done = False

        self.width = width
        self.height = height

        self.fbo = Framebuffer()

        t = 0.0
        self.view = np.matmul(translationMatrix([0, 0, t]), rotationMatrixX(-np.pi/2.0))

        self.bind()

        glTexImage2D(GL_TEXTURE_2D, 0, self.format, width, height, 0, self.format, self.type, None)

        self.fbo.prepare(self, GL_TEXTURE_2D)

        self.unbind()

    def update(self, scene):
        if self.done:
            return

        self.bind()

        Pscene = scene.P

        scene.P = frustumMatrix(-1.0, +1.0, -1.0, +1.0, 1.0, 20.0)

        glViewport(0, 0, self.width, self.height)

        self.fbo.bind()
        
        scene.camera.V = self.view

        scene.draw_reflections()

        scene.camera.update()

        self.fbo.unbind()

        # reset the viewport
        glViewport(0, 0, scene.window_size[0], scene.window_size[1])

        scene.P = Pscene

        self.unbind()



#class EnvironmentBox(DrawModelFromMesh):
#    def __init__(self, scene, shader=EnvironmentShader(), width=200, height=200):
#        self.done = False

        #self.map = EnvironmentMappingTexture(width, height)

        #DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(), mesh=CubeMesh(shader.map), shader=shader, visible=False)
