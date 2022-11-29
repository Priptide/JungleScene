

from ShadowMapping import lookAt
from texture import Texture
from OpenGL.GL import *
from matutils import *

from mesh import Mesh
from BaseModel import DrawModelFromMesh
from shaders import BaseShaderProgram,PhongShader
from texture import Texture
from framebuffer import Framebuffer


class ReflectionMappingTexture(Texture):
    def __init__(self, width=200, height=200):

        self.name = 'reflection'
        self.format = GL_RGBA
        self.type = GL_UNSIGNED_BYTE
        self.wrap = GL_CLAMP_TO_EDGE
        self.sample = GL_LINEAR
        self.target = GL_TEXTURE_2D
        self.width = width
        self.height = height


        self.textureid = glGenTextures(1)

        self.bind()
        glTexImage2D(self.target, 0, self.format, self.width, self.height, 0, self.format, self.type, None)
        self.unbind()

        self.set_wrap_parameter(self.wrap)
        self.set_sampling_parameter(self.sample)
        # self.set_shadow_comparison()

        self.fbo = Framebuffer(texture=self)

        self.V = None

    def update(self, scene, plane):
        # backup the view matrix and replace with the new one

        self.bind()

        # Pscene = scene.P

        # scene.P = frustumMatrix(-1.0, +1.0, -1.0, +1.0, 1.0, 20.0)

        # update the viewport for the image size
        glViewport(0, 0, self.width, self.height)

        self.fbo.bind()

        self.psi = scene.camera.psi
        scene.camera.psi = -self.psi
        scene.camera.update()
        scene.draw_reflections(plane=plane)

        self.fbo.unbind()

        scene.camera.psi = self.psi
        scene.camera.update()

        # reset the viewport to the windows size
        glViewport(0, 0, scene.window_size[0], scene.window_size[1])
        
        # scene.P = Pscene

        self.unbind()