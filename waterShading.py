from BaseModel import BaseModel,DrawModelFromMesh
from mesh import *

from OpenGL.GL.framebufferobjects import *

from cubeMap import CubeMap

from shaders import *

from framebuffer import Framebuffer


class WaterShader(BaseShaderProgram):
    def __init__(self, reflection_texture=None, refraction_texture=None, name='water'):
        BaseShaderProgram.__init__(self, name=name)
        self.add_uniform('sampler_cube')
        self.add_uniform('VM')
        self.add_uniform('VMiT')
        self.add_uniform('VT')
        self.add_uniform('plane')
        self.add_uniform('reflectionTexture')
        self.add_uniform('refractionTexture')
        self.reflection_texture = reflection_texture
        self.refraction_texture = refraction_texture

    def bind(self, model, M, plane=np.array([0, -1, 0, 10000], 'f'),):

        
        glUseProgram(self.program)

        # self.reflection_texture_pos = glGetUniformLocation(self.program, "reflectionTexture")
        # self.refraction_texture_pos = glGetUniformLocation(self.program, "refractionTexture")
        # glUniform1i(self.reflection_texture_pos, 0)
        # glUniform1i(self.refraction_texture_pos, 1)

        # glActiveTexture(GL_TEXTURE0)
        # glBindTexture(GL_TEXTURE_2D, self.reflection_texture)
        # print(GL_TEXTURE0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.refraction_texture)


        P = model.scene.P  # get projection matrix from the scene
        V = model.scene.camera.V  # get view matrix from the camera

        # set the PVM matrix uniform
        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))

        # set the PVM matrix uniform
        self.uniforms['VM'].bind(np.matmul(V, M))

        # set the PVM matrix uniform
        self.uniforms['VMiT'].bind(np.linalg.inv(np.matmul(V, M))[:3, :3].transpose())

        self.uniforms['VT'].bind(V.transpose()[:3, :3])

        # self.uniforms[]


class WaterFBO():
    def __init__(self, screen_width=200, screen_height=200):

        self.done = False

        self.width = screen_width
        self.height = screen_height

        self.reflection_width = 200
        self.reflection_height = 200
        self.refraction_width = 200
        self.refraction_height = 200
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initialiseReflectionFrameBuffer()
        self.initialiseRefractionFrameBuffer()
        

    def unbindCurrentFrameBuffer(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, self.screen_width, self.screen_height)

    def initialiseReflectionFrameBuffer(self):
        self.reflectionFrameBuffer = self.createFrameBuffer()
        self.reflectionTexture = self.createTextureAttachment(self.reflection_width,self.reflection_height)
        self.reflectionDepthBuffer = self.createDepthBufferAttachment(self.reflection_width,self.reflection_height)
        self.unbindCurrentFrameBuffer()
	
    def initialiseRefractionFrameBuffer(self):
        self.refractionFrameBuffer = self.createFrameBuffer()
        self.refractionTexture = self.createTextureAttachment(self.refraction_width,self.refraction_height)
        self.refractionDepthTexture = self.createDepthTextureAttachment(self.refraction_width,self.refraction_height)
        self.unbindCurrentFrameBuffer()

    def bindFrameBuffer(self, frameBuffer, width, height):
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer)
        glViewport(0, 0, width, height)

    def createFrameBuffer(self):
        frameBuffer = glGenFramebuffers(1)
        #Give the frame buffer a name
        glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer)
        #Always add a color attachment
        glDrawBuffer(GL_COLOR_ATTACHMENT0)
        return frameBuffer

    def createTextureAttachment(self, width, height):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,texture, 0)
        return texture

    def createDepthTextureAttachment(self, width, height):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT32, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, texture, 0)
        return texture

    def createDepthBufferAttachment(self, width, height):
        depthBuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depthBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthBuffer)
        return depthBuffer

    def bindRefractionFrameBuffer(self):
        self.bindFrameBuffer(self.refractionFrameBuffer,self.refraction_width,self.reflection_height)

    def bindReflectionFrameBuffer(self):
        self.bindFrameBuffer(self.reflectionFrameBuffer,self.reflection_width,self.reflection_height)

	