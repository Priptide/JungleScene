
# import the scene class
from random import randint
from BaseModel import DrawModelFromMesh
from CoverModel import Cover
from FloorModel import Floor
from Parcticles import ParticleRenderer
from PondModel import Pond
from RefractionMapping import RefractionMappingTexture
from WaterModel import Water
from blender import load_obj_file
from lightSource import LightSource
from ReflectionMapping import ReflectionMappingTexture
from scene import Scene
from OpenGL.GL import *
from matutils import *
import pygame
from shaders import *
from skyBox import SkyBox
from texture import Texture

class JungleScene(Scene):
    def __init__(self):

        self.width = 100
        self.height = 100
        Scene.__init__(self)

        self.skybox = SkyBox(scene=self)

        #Set up reflection and refraction mapping textures
        self.reflection = ReflectionMappingTexture(width=400, height=400)
        self.refraction = RefractionMappingTexture(width=400, height=400)
        
        #Set up the models for our floor, pond and base
        self.floor = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-225, 0.2, -225]), mesh=Floor(width=45, height=45, textures=[Texture('StyleGrass.jpg'), Texture('Stylized_Grass_normal.jpg'), Texture('Stylized_Grass_height.png')]), shader=TerrainShader())
        self.pond = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-95, -0.3, -95]), mesh=Pond(width=19, height=19, textures=[Texture('Sand.jpg'), Texture('Sand_normal.jpg'), Texture('Sand_height.png')]), shader=TerrainShader())
        self.base = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-225, -0.1, -225]), mesh=Cover(width=45, height=45), shader=FlatShader())
       
        #Set up the water with a reflection and refraction texture
        self.water = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, -0.1, -100]), mesh=Water(width=20,height=20, textures=[self.reflection, self.refraction, Texture("waterdudv.jpg")]), shader=WaterShader())
        
        #Load all our models and objects in the scene
        self.objects = []
        # tree_2 = load_obj_file("./models/Tropical_2.obj")
        # tree_3 = load_obj_file("./models/Tropical_3.obj")
        # tree_4 = load_obj_file("./models/Tropical_4.obj")
        # bush_1 = load_obj_file("./models/Bush_1.obj")
        # bush_2 = load_obj_file("./models/Bush_2.obj")
        # bush_3 = load_obj_file("./models/Bush_3.obj")
        # plant_1 = load_obj_file("./models/Plant_1.obj")
        # totem = load_obj_file("./models/Totem.obj")
        # totem_main = load_obj_file("./models/TongueTotem.obj")
        campfire = load_obj_file("./models/campfire.obj")
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[100, 0.2, 0],orientation=210,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.2, 0], orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_2])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-120, 0.2, 50], orientation=300,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-140, 0.2, 80], orientation=210,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-80, 0.2, -100],orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_2])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[150, 0.2, 80], orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_3])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[100, 0.2, -100], orientation=0,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_3])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[70, 0.2, 110], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[120, 0.2,-30], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-160, 0.2,-120], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_2])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.2, 150], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_3])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[120, 0.2, 140], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_2])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-85, 0.2, 0], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-80, 0.2, 34], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-72, 0.2, 73], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-23, 0.2, 84], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[30, 0.2, 82], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[83, 0.2, 30], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[72, 0.2, 67], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[50, 0.2, -130], orientation=100,scale=.2), mesh=mesh, shader=PhongShader())) for mesh in totem])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-50, 0.2, -130], orientation=-100,scale=.2), mesh=mesh, shader=PhongShader())) for mesh in totem])
        # self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 0.2, -180], orientation=0,scale=.4), mesh=mesh, shader=PhongShader())) for mesh in totem_main])
        self.objects.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 0.2, 120], orientation=0,scale=30), mesh=mesh, shader=PhongShader())) for mesh in campfire])
        
        #Set up a light source over the campfire model
        self.light = LightSource(self, position=[0, 15, 117], Ia=[0.4,0.4,0.4], Id=[1.85,1.7,0.8], Is=[0.85, 0.6, 0.1])

        #Set up a particle effect over the campfire
        self.particles = ParticleRenderer(scene=self, count=10, origin=np.array([0, 10, 115.5]), max_x=10, min_x=-10, max_z=10, min_z=-10)


    def draw_reflections(self, plane):
        '''
        Draw all objects in the scene into the reflection framebuffer
        '''

        self.skybox.draw(plane=plane)
        self.floor.draw(plane=plane)
        self.pond.draw(plane=plane)
        
        for model in self.objects:
            model.draw(plane=plane)
        
        self.particles.update(scene=self, plane=plane)

    def draw_refractions(self, plane):
        '''
        Draw all objects in the scene into the refraction framebuffer ignoring particles
        '''
        self.skybox.draw(plane=plane)
        self.floor.draw(plane=plane)
        self.pond.draw(plane=plane)
        
        for model in self.objects:
            model.draw(plane=plane)


    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        '''

        # Clear the color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Update the camera
        self.camera.update()

        # Draw the skybox
        self.skybox.draw()
        
        # Enable clip distance for fbo processing
        glEnable(GL_CLIP_DISTANCE0)

        # Process reflection and refraction framebuffers updating our culling plane
        self.reflection.update(scene=self, plane=np.array([0, 1, 0, -0.1], 'f'))
        self.refraction.update(scene=self, plane=np.array([0, -1, 0, 0.1], 'f'))
        
        # Disable clip distances, we also default far planes in case this doesn't work
        glDisable(GL_CLIP_DISTANCE0)

        #Draw models in the scene
        self.floor.draw()
        self.pond.draw()
        self.base.draw()
        
        #Draw loaded in objects
        for obj in self.objects:
            obj.draw()


        #Draw the water plane and update it's speed
        self.water.draw()
        self.water.shader.update(speed=0.02)

        #Update the particles
        self.particles.update(scene=self)


        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

if __name__ == '__main__':

    scene = JungleScene()

    scene.run()