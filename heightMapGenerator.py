

from collections import deque
from enum import Enum
from math import floor
from random import randint
import numpy as np

moves = [[0,1], [0,-1],[1,0],[-1,0], [1,1],[-1,-1],[-1,1],[1,-1]]

def generate(width=100, height=100, poi=2, gradient = 0.01):
  points = np.zeros((height, width), 'f')
  #pick two high points
  min_x = 0
  min_y = 0
  max_x = floor(width/poi)
  max_y = floor(height/poi)
  placed = []
  queue = deque()
  while(poi > 0):
    x_cord = randint(min_x, max_x-1)
    y_cord = randint(min_y, max_y-1)
    min_x = max_x
    min_y = max_y
    max_x = max_x+floor(width/poi)
    max_y = max_y+floor(height/poi)
    points[y_cord][x_cord] = randint(-10,-4)
    placed.append(([y_cord,x_cord]))
    queue.append(([y_cord,x_cord]))
    poi-=1

  while(len(queue) > 0):
    local = queue.pop()

    for i in moves:
      point_y = local[0]+i[0]
      point_x = local[1]+i[1]
      if(placed.count(([point_y,point_x])) == 0 and point_x >= 0 and point_x < width and point_y >= 0 and point_y < height):
        points[point_y][point_x] = max(points[point_y][point_x], points[local[0]][local[1]] + gradient)
        placed.append(([point_y,point_x]))
        queue.append(([point_y,point_x]))
  
  return points