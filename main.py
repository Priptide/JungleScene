
# import the scene class
from random import randint
from BaseModel import DrawModelFromMesh
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
from sphereModel import Sphere
import pywavefront
from pywavefront import visualization

class JungleScene(Scene):
    def __init__(self):
        self.width = 100
        self.height = 100
        scale = 10
        Scene.__init__(self, terrain_width=self.width, terrain_height=self.height)

        self.light = LightSource(self, position=[0, -100, 0])

        self.shaders='phong'

        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)
        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=2), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())
        self.terrain = DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 0, 0]), mesh=Terrain(width=self.width, height=self.height), shader=PhongShader())
        self.terrain_items = []

        self.tree = pywavefront.Wavefront('./models/bunny_world.obj', collect_faces=True)
        # self.tree = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0,0,0]), scaleMatrix([0.5,0.5,0.5])), mesh=tree[0], shader=FlatShader())
        #generate all terrain items
        self.generate_jungle()

    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.terrain.draw()
        # also all models from the table
        for model in self.terrain_items:
            model.draw()

        # # and for the box
        # for model in self.box:
        #     model.draw()

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
                local_model = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.terrain.mesh.vertices[vertex], scale=10), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())
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

            
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            # self.environment.update(self)
            visualization.draw(self.tree)
            self.terrain.draw()
        # then we loop over all models in the terrain list and draw them
        for model in self.terrain_items:
            model.draw()

        self.show_light.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

if __name__ == '__main__':

    scene = JungleScene()

    scene.run()