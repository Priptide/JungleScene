
# import the scene class
from random import randint
from BaseModel import DrawModelFromMesh
from FloorModel import Floor
from PondModel import Pond
from ShadowMapping import *
from TerrainModel import Terrain
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

class JungleScene(Scene):
    def __init__(self):
        self.width = 100
        self.height = 100
        scale = 10
        Scene.__init__(self)

        self.light = LightSource(self, position=[0, 500, 0])

        self.shaders='phong'

        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)
        self.skybox = SkyBox(scene=self)
        # self.terrain = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-(self.width/2)*10, 0, -(self.height/2)*10]), mesh=Terrain(width=self.width, height=self.height), shader=PhongShader())
        self.floor = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-200, 0.2, -200]), mesh=Floor(width=40, height=40), shader=PhongShader())
        self.pond = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.1, -100]), mesh=Pond(width=20, height=20), shader=PhongShader())
        self.terrain_items = []

        self.plants = []
        tree_2 = load_obj_file("./models/Tropical_2.obj")
        tree_3 = load_obj_file("./models/Tropical_3.obj")
        tree_4 = load_obj_file("./models/Tropical_4.obj")
        bush_1 = load_obj_file("./models/Bush_1.obj")
        bush_2 = load_obj_file("./models/Bush_2.obj")
        bush_3 = load_obj_file("./models/Bush_3.obj")
        plant_1 = load_obj_file("./models/Plant_1.obj")
        totem = load_obj_file("./models/Totem.obj")
        totem_main = load_obj_file("./models/TongueTotem.obj")
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[100, 0.2, 0],orientation=210,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.2, 0], orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_2])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-120, 0.2, 50], orientation=300,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-140, 0.2, 80], orientation=210,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-80, 0.2, -100],orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_2])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[150, 0.2, 80], orientation=180,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_3])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[100, 0.2, -100], orientation=0,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_3])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[70, 0.2, 110], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in tree_4])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[120, 0.2,-30], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-160, 0.2,-120], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_2])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-100, 0.2, 150], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_3])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[120, 0.2, 140], orientation=220,scale=10), mesh=mesh, shader=PhongShader())) for mesh in bush_2])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-85, 0.2, 0], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-80, 0.2, 34], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-72, 0.2, 73], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-23, 0.2, 84], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[30, 0.2, 82], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[83, 0.2, 30], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[72, 0.2, 67], orientation=220,scale=8), mesh=mesh, shader=PhongShader())) for mesh in plant_1])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[50, 0.2, -130], orientation=100,scale=.2), mesh=mesh, shader=PhongShader())) for mesh in totem])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[-50, 0.2, -130], orientation=-100,scale=.2), mesh=mesh, shader=PhongShader())) for mesh in totem])
        self.plants.extend([(DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 0.2, -150], orientation=0,scale=.4), mesh=mesh, shader=PhongShader())) for mesh in totem_main])
        #generate all terrain items
        # self.generate_jungle()

    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # self.terrain.draw()

        self.floor.draw()
        self.pond.draw()
        # also all models from the table
        for model in self.terrain_items:
            model.draw()

        # # and for the box
        # for model in self.box:
        #     model.draw()
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

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        self.skybox.draw()
            
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            # self.environment.update(self)
            # self.terrain.draw()
            
            self.floor.draw()
            self.pond.draw()
            for obj in self.plants:
                obj.draw()
        # then we loop over all models in the terrain list and draw them
        for model in self.terrain_items:
            model.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

if __name__ == '__main__':

    scene = JungleScene()

    scene.run()