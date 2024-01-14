import math
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Planet:
    def __init__(self, name, color, radius, distance, speed):
        self.name = name
        self.color = color
        self.radius = radius
        self.distance = distance
        self.speed = speed
        self.angle = 0.0

    def draw(self):
        num_segments = 1000 
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments):
            theta = 2.0 * math.pi * float(i) / num_segments
            dx = self.distance * math.cos(theta)
            dy = self.distance * math.sin(theta)
            glVertex3f(dx, dy, 0.0)
        glEnd()
        glPushMatrix()
        glColor3f(self.color[0], self.color[1], self.color[2])
        glRotatef(self.angle, 0.0, 0.0, 1.0) #rotates the obj around z axis
        glTranslatef(self.distance, 0.0, 0.0)
        gluSphere(gluNewQuadric(), self.radius, 32, 32) #draws a sphere

        # Draw rings if the planet is Saturn
        if self.name == "Saturn":
            glColor3f(0.8, 0.8, 0.6)  # Color of the rings
            for i in np.linspace(self.radius + 0.1, self.radius + 0.3, 2):  # Two rings
                glBegin(GL_LINE_LOOP)
                for theta in np.linspace(0, 2 * np.pi, 100):
                    x = i * np.cos(theta)
                    y = i * np.sin(theta)
                    glVertex3f(x, y, 0.0)
                glEnd()

        glPopMatrix()

    def update_position(self):
        self.angle += self.speed
class Moon:
    def __init__(self, planet, distance, radius, speed, color):
        self.planet = planet
        self.distance = distance
        self.radius = radius
        self.speed = speed
        self.color = color
        self.angle = 0

    def update_position(self):
        self.angle += self.speed
        if self.angle > 360:
            self.angle -= 360

    def draw(self):
        glPushMatrix()
        glColor3f(self.color[0], self.color[1], self.color[2])
        glRotatef(self.planet.angle, 0.0, 0.0, 1.0)
        glTranslatef(self.planet.distance, 0.0, 0.0)
        glRotatef(self.angle, 0.0, 0.0, 1.0)
        glTranslatef(self.distance, 0.0, 0.0)
        gluSphere(gluNewQuadric(), self.radius, 32, 32)
        glPopMatrix()
class Meteor:
    def __init__(self, color, radius, speed):
        self.color = color
        self.radius = radius
        self.speed = speed
        self.angle = np.random.uniform(0.0, 360.0)
        self.distance = np.random.uniform(15, 20.0)

    def draw(self):
        glColor3f(self.color[0], self.color[1], self.color[2])
        glPushMatrix()
        glRotatef(self.angle, 0.0, 0.0, 1.0)
        glTranslatef(self.distance, 0.0, 0.0)
        gluSphere(gluNewQuadric(), self.radius, 32, 32)
        glPopMatrix()

    def update_position(self):
        self.angle += self.speed

class SolarSystem:
    def __init__(self):
        earth = Planet("Earth", (0.0, 0.5, 1.0), 0.7, 10.0, 2.5)
        moon = Moon(earth, 2.0, 0.1, 2.0, (1.0, 1.0, 1.0))
        earth.moons = [moon]

        self.planets = [
            Planet("Sun", (1.0, 1.0, 0.0), 1.0, 0.0, 0.1), #color, radius, distance, speed
            Planet("Mercury", (0.6, 0.3, 0.0), 0.5, 4.0, 4.0),  
            Planet("Venus", (0.5, 0.2, 0.5), 0.6, 7.0, 3.0),  
            earth,  
            Planet("Mars", (1.0, 0.0, 0.0), 0.6, 15.0, 2.0),  
            Planet("Jupiter", (0.9, 0.7, 0.5), 1.3, 20.0, 1.3),  
            Planet("Saturn", (0.9, 0.7, 0.5), 1.2, 25.0, 1.0),  
            Planet("Uranus", (0.0, 0.5, 0.5), 1.2, 29.0, 0.3),  
            Planet("Neptune", (0.0, 0.0, 1.0), 1.2, 34.0, 0.2),  
            Planet("Pluto", (0.5, 0.5, 0.5), 0.4, 40.0, 0.1),
        ]
        self.meteors = [Meteor((0.5, 0.5, 0.5), 0.1, np.random.uniform(0.1, 1.5)) for _ in range(100)]

    def update_positions(self):
        for planet in self.planets:
            planet.update_position()
            if hasattr(planet, 'moons'):
                for moon in planet.moons:
                    moon.update_position()
        for meteor in self.meteors:
            meteor.update_position()

    def draw(self):
        for planet in self.planets:
            planet.draw()
            if hasattr(planet, 'moons'):
                for moon in planet.moons:
                    moon.draw()
        for meteor in self.meteors:
            meteor.draw()
class Star:
    def __init__(self):
        self.color = (np.random.uniform(1.0, 0.0), np.random.uniform(1.0, 0.0), np.random.uniform(1.0, 0.0))
        self.position = (np.random.uniform(-40.0, 40.0), np.random.uniform(-40.0, 40.0), np.random.uniform(-40.0, 40.0))

    def draw(self):
        glColor3f(*self.color)
        glVertex3f(*self.position)

stars = [Star() for _ in range(500)]  # Generate stars once

def draw_stars():
    glPointSize(0.5)
    glBegin(GL_POINTS)
    for star in stars:  # Draw each star
        star.draw()
    glEnd()

def main():
    pygame.init()
    display = (400, 400)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(500, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    solar_system = SolarSystem()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_stars()
        solar_system.update_positions()
        solar_system.draw()
        pygame.display.flip()
        pygame.time.wait(30)

if __name__ == "__main__":
    main()
