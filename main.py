
# import the scene class
from random import randint
from BaseModel import DrawModelFromMesh
from FloorModel import Floor
from Parcticles import ParticleRenderer
from PondModel import Pond
from ShadowMapping import *
from TerrainModel import Terrain
from WaterModel import Water
from blender import load_obj_file
from lightSource import LightSource
from scene import Scene
from OpenGL.GL import *
from matutils import *
import pygame
from shaders import *
from environmentMapping import *
from skyBox import SkyBox
from sphereModel import Sphere
import pywavefront
from waterShading import WaterFBO, WaterShader

class JungleScene(Scene):
    def __init__(self):
        self.width = 100
        self.height = 100
        scale = 10
        Scene.__init__(self)

        # self.light = LightSource(self, position=[0, 2, 0])

        self.shaders='phong'

        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)
        self.skybox = SkyBox(scene=self)
        # self.environment = EnvironmentMappingTexture(width=200, height=200)
        # self.refraction = EnvironmentMappingTexture(width=200, height=200)
        # self.terrain = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-(self.width/2)*10, 0, -(self.height/2)*10]), mesh=Terrain(width=self.width, height=self.height), shader=PhongShader())
        self.floor = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-200, 0.2, -200]), mesh=Floor(width=40, height=40), shader=PhongShader())
        self.pond = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.1, -100]), mesh=Pond(width=20, height=20), shader=PhongShader())
        # self.water_fbo = WaterFBO(screen_width=self.window_size[0], screen_height=self.window_size[1])
        # self.water_mesh = Water(width=20,height=20)
        # self.water = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.1, -100]), mesh=Water(width=20,height=20), shader=EnvironmentShader(map=self.environment))
        self.terrain_items = []
        self.plants = []
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
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[100, 0.2, 0],orientation=210,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.2, 0], orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_2])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-120, 0.2, 50], orientation=300,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-140, 0.2, 80], orientation=210,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-80, 0.2, -100],orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_2])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[150, 0.2, 80], orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_3])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[100, 0.2, -100], orientation=0,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_3])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[70, 0.2, 110], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[120, 0.2,-30], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-160, 0.2,-120], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_2])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.2, 150], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_3])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[120, 0.2, 140], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_2])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-85, 0.2, 0], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-80, 0.2, 34], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-72, 0.2, 73], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-23, 0.2, 84], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[30, 0.2, 82], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[83, 0.2, 30], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[72, 0.2, 67], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[50, 0.2, -130], orientation=100,scale=.2), mesh=mesh, shader=PhongShader())) for mesh in totem])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-50, 0.2, -130], orientation=-100,scale=.2), mesh=mesh, shader=PhongShader())) for mesh in totem])
        # self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 0.2, -180], orientation=0,scale=.4), mesh=mesh, shader=PhongShader())) for mesh in totem_main])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 0.2, -105], orientation=0,scale=30), mesh=mesh, shader=FlatShader())) for mesh in campfire])
        self.light = LightSource(self, position=[0, 15, -102], Ia=[0.4,0.4,0.4], Id=[1.85,1.7,0.8], Is=[0.85, 0.6, 0.1])
        self.particles = ParticleRenderer(scene=self, count=10, origin=np.array([0, 10, -100.5]), max_x=10, min_x=-10, max_z=10, min_z=-10)
        
        
        #generate all terrain items
        # self.generate_jungle()

    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # self.terrain.draw()

        self.floor.draw()
        self.pond.draw()


        # for model in self.terrain_items:
        #     model.draw()

        # # and for the box
        # for model in self.box:
        #     model.draw()
        for model in self.plants:
            model.draw()

    def draw_reflections(self):
        self.skybox.draw()
        self.floor.draw()
        self.pond.draw()
        
        for model in self.plants:
            model.draw()

    def generate_jungle(self, num_items = 10):

        locations = []
        #Iterate till all items are placed
        while num_items > 0:
            #Pick random coordinate between 1 row up and terrain size 1 row down as we don't want an edge
            vertex = randint(self.height+1, len(self.terrain.mesh.vertices)-self.height)

            if vertex % self.height == 0 or (vertex+1) % self.height == 0:
                continue
            #Check no item is placed here
            if vertex not in locations:
                locations.append(vertex)
                pos = [self.terrain.mesh.vertices[vertex][0]-(self.width/2)*10, self.terrain.mesh.vertices[vertex][1], self.terrain.mesh.vertices[vertex][2]-(self.height/2)*10]
                local_model = DrawModelFromMesh(scene=self, M=poseMatrix(position=pos, scale=10), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())
                self.terrain_items.append(local_model)
                num_items-=1


    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # glEnable(GL_CLIP_DISTANCE0)

        # self.water_fbo.bindReflectionFrameBuffer()
        # np.set_printoptions(precision=3)
        # np.set_printoptions(suppress=True)
        # dist = 2*self.camera.V[1][3] - self.water.M[1][3]
        # self.camera.V[1][3] -= dist
        # self.camera.psi = -self.camera.psi
        # self.camera.phi = -self.camera.phi


        # current_plane = np.array([0,1,0,-self.water.M[1][3]],'f')

        # self.skybox.draw(plane=current_plane)
        # self.floor.draw(plane=current_plane)
        # # self.pond.draw(plane=current_plane)
        
        # for obj in self.plants:
        #     obj.draw(plane=current_plane)

        # self.camera.V[1][3] += dist
        # self.camera.psi = -self.camera.psi
        # self.camera.phi = -self.camera.phi
        # self.camera.update()

        # self.water_fbo.bindRefractionFrameBuffer()

        # current_plane = np.array([0,-1,0,self.water.M[1][3]],'f')

        # self.skybox.draw(plane=current_plane)
        # self.floor.draw(plane=current_plane)
        # self.pond.draw(plane=current_plane)
        
        # for obj in self.plants:
        #     obj.draw(plane=current_plane)
        
        # self.water_fbo.unbindCurrentFrameBuffer()

        # glDisable(GL_CLIP_DISTANCE0)


        self.camera.update()
        self.shadows.render(self)
        self.skybox.draw()
        # when rendering the framebuffer we ignore the reflective object
        # if not framebuffer:
        #     glEnable(GL_CLIP_DISTANCE0)
        # self.environment.update(self)
        #     self.refraction.update(self, plane=np.array([0,-1,0,self.water.M[1][3]],'f'))
        #     glDisable(GL_CLIP_DISTANCE0)
            # self.terrain.draw()
        self.floor.draw()
        self.pond.draw()
        # self.water.draw()
        for obj in self.plants:
            obj.draw()

        self.particles.update(scene=self)

        # self.water.draw()
        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

if __name__ == '__main__':

    scene = JungleScene()

    scene.run()