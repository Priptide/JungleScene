from texture import Texture
from OpenGL.GL import *
from matutils import *
from texture import Texture
from framebuffer import Framebuffer


class ReflectionMappingTexture(Texture):
    '''
    Used to create a reflection texture of the scene
    '''
    def __init__(self, width=200, height=200):
        
        #Setup a new texture
        self.name = 'reflection'
        self.format = GL_RGBA
        self.type = GL_UNSIGNED_BYTE
        self.wrap = GL_CLAMP_TO_EDGE
        self.sample = GL_LINEAR
        self.target = GL_TEXTURE_2D
        self.width = width
        self.height = height

        #Generate a new texture id
        self.textureid = glGenTextures(1)

        #Bind this texture too a 2d texture
        self.bind()
        glTexImage2D(self.target, 0, self.format, self.width, self.height, 0, self.format, self.type, None)
        self.unbind()

        #Set our wrap and sampling parameter
        self.set_wrap_parameter(self.wrap)
        self.set_sampling_parameter(self.sample)

        #Set up a framebuffer to output to our this texture
        self.fbo = Framebuffer(texture=self)

    def update(self, scene, plane):
        
        #Bind this texture
        self.bind()

        # update the viewport for the image size
        glViewport(0, 0, self.width, self.height)

        #Bind the framebuffer to be the current frame buffer
        self.fbo.bind()

        #Save our current angle too the horizontal
        self.psi = scene.camera.psi

        #Move our camera to be at the opposite angle to the horizontal (below it)
        scene.camera.psi = -self.psi
        scene.camera.update()

        #Draw all the objects in the scene too our texture
        scene.draw_reflections(plane=plane)

        #Unbind the framebuffer from the scene
        self.fbo.unbind()

        #Return our camera too the same position
        scene.camera.psi = self.psi
        scene.camera.update()

        # reset the viewport to the windows size
        glViewport(0, 0, scene.window_size[0], scene.window_size[1])
        
        #unbind the current texture
        self.unbind()