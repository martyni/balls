import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.GL.ARB.occlusion_query import *
from OpenGL.GL.HP.occlusion_test import *
from OpenGL.GLUT import glutSolidCube
import numpy as np
import math
from banner import banner

from random import randint

pygame.init()
WIDTH,HEIGHT = 1920, 1080
display = (WIDTH, HEIGHT) 
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

sphere = gluNewQuadric() 

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# init mouse movement and center mouse on screen
displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
run = True




def event_handling(run):
    paused = False
    run = True
    mouseMove = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter) 
        if not paused: 
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)    
    return paused, run, mouseMove



X,Y,Z = [0,0,0]
SPEED = 1

def cycle(speed=500, offset=0, function=math.sin):
    source = pygame.time.get_ticks()/speed
    return function(source + offset)



def draw_crosshair_in_2d():
    glPushMatrix()
    '''
    glViewport(0, 0, WIDTH, HEIGHT)'''
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3ub(240, 240, 240)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2i(int(WIDTH / 2 - 7), int(HEIGHT / 2))
    glVertex2i(int(WIDTH / 2 + 7), int(HEIGHT / 2))
    glEnd()
    glBegin(GL_LINES)
    glVertex2i(int(WIDTH / 2), int(HEIGHT / 2 + 7))
    glVertex2i(int(WIDTH / 2), int(HEIGHT / 2 - 7))
    glEnd()
    glPopMatrix()


def draw_crosshair_3d():
    crosshair = np.array([
      -0.02, 0,
       0.02, 0,
       0, -0.02,
       0,  0.02], dtype = 'float32')
    vbo_2d, vao_2d = glGenBuffers(1), glGenVertexArrays(1)
    
    glBindVertexArray(vao_2d)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_2d)
    glBufferData(GL_ARRAY_BUFFER, crosshair, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
        #render 3d stuff with another shader program and other vbos ad vaos
    
    glBindVertexArray(0)

    
    '''shader_program_2d.use()'''
    glBindVertexArray(vao_2d)
    glDrawArrays(GL_LINES, 0, 4)

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()
    glLoadIdentity()                                   # reset position

    glColor3f(0.0, 0.0, 1.0)                           # set color to blue

def draw_floor():
    glPushMatrix()
    glColor4f(0.5, 0.5, 0.5, 1)
    glBegin(GL_QUADS)
    glVertex3f(-10, -10, -2)
    glVertex3f(10, -10, -2)
    glVertex3f(10, 10, -2)
    glVertex3f(-10, 10, -2)
    glEnd()

def draw_fake_floor():
    glPushMatrix()
    glColor4f(0.5, 0.5, 0.5, 1)
    glBegin(GL_QUADS)
    glEnd()

def draw_ball(x, y, z, r, g, b, mouseMove, viewMatrix, size=1.0, k=32, l=16):
    glTranslatef(x, y, z)
    glColor4f(r, g, b, 1)
    gluSphere(sphere, size, k, l) 
    glTranslatef(-x, -y, -z)



while run:
    paused, run, mouseMove = event_handling(run)
    if not paused:
        # get keys
        keypress = pygame.key.get_pressed()
        #mouseMove = pygame.mouse.get_rel()
    
        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        up_down_angle += mouseMove[1]*SPEED
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movment 
        if keypress[pygame.K_w]:
            glTranslatef(0,0,SPEED)
            Z += SPEED
        if keypress[pygame.K_s]:
            glTranslatef(0,0,-SPEED)
            Z -= SPEED
        if keypress[pygame.K_d]:
            glTranslatef(-SPEED,0,0)
            X -= SPEED
        if keypress[pygame.K_a]:
            glTranslatef(SPEED,0,0)
            X += SPEED

        if keypress[pygame.K_UP]:
            #glTranslatef(0,-SPEED,0)
            #Y -= SPEED
            glRotatef(-SPEED*10, 0.0, 0.0, 1.0)
        if keypress[pygame.K_DOWN]:
            #glTranslatef(0,SPEED,0)
            #Y += SPEED
            glRotatef(SPEED*10, 0.0, 0.0, 1.0)
        if keypress[pygame.K_RIGHT]:
            glRotatef(SPEED*10, 0.0, 1.0, 0.0)
        if keypress[pygame.K_LEFT]:
            glRotatef(-SPEED*10, 0.0, 1.0, 0.0)
        # apply the left and right rotation
        glRotatef(mouseMove[0]*SPEED, 0.0, 1.0, 0.0)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix 
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #draw_floor()
        draw_fake_floor()

        #draw_ball(0.5 - X, 1 + Z, Y , 1 , 0 , 0  , mouseMove, viewMatrix ) 
        #draw_ball(2 - X, 1 + Z, Y , 0 , 0.5 , 0  , mouseMove, viewMatrix ) 
        #draw_ball(-3.0 - X,  Z, Y , 0 , 0.5 , 0  , mouseMove, viewMatrix ) 
        #draw_ball(-3 - X,  0, Y , 0 , 1 , 0  , mouseMove, viewMatrix ) 
        #draw_ball(0,  0, -Z , 0 , 0 , 1  , mouseMove, viewMatrix ) 
        #draw_ball(0,  0, 0 , 0.5 , 0.5 , 0  , mouseMove, viewMatrix , -Z) 
        #draw_ball(0,  0, 0 , 0.0 , 0.5 , 0.5  , mouseMove, viewMatrix , -X) 
        #draw_rect(5 , 3, WIDTH, HEIGHT )
        lines = [ line for line in banner.split('\n') ]


        for y in range(0, len(lines)):
           for x in range(0, len(lines[0])):
              for z in range(0, 1):
                  if lines[y][x] !=' ' and lines[y][x] !='_':
                     #draw_ball(x, z, y, math.cos(x), math.sin(y), math.sin(z), mouseMove, viewMatrix) 
                     draw_ball(x/2, -z * 2, -y, math.sin(x), math.cos(y), 2, mouseMove, viewMatrix,0.3) 
        glEnable(GL_CULL_FACE)
        glMatrixMode(GL_MODELVIEW)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()
