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
        num_segments = 100
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
        glRotatef(self.angle, 0.0, 0.0, 1.0)
        glTranslatef(self.distance, 0.0, 0.0)
        gluSphere(gluNewQuadric(), self.radius, 32, 32)

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
class SolarSystem:
    def __init__(self):
        self.planets = [
            Planet("Sun", (1.0, 1.0, 0.0), 1.0, 0.0, 0.0),
            Planet("Mercury", (0.5, 0.5, 0.5), 0.5, 4.0, 4.0),
            Planet("Venus", (0.9, 0.6, 0.2), 0.6, 7.0, 3.0),
            Planet("Earth", (0.0, 0.0, 1.0), 0.7, 10.0, 2.5),
            Planet("Mars", (1.0, 0.0, 0.0), 0.6, 15.0, 2.0),
            Planet("Jupiter", (0.9, 0.7, 0.5), 1.3, 20.0, 1.3),
            Planet("Saturn", (0.9, 0.8, 0.6), 1.2, 25.0, 1.0),
            Planet("Uranus", (0.0, 0.5, 0.5), 2.4, 28.0, 0.3),
            Planet("Neptune", (0.4, 0.5, 0.5), 2.1, 32.0, 0.2),
            Planet("Pluto", (0.5, 0.5, 0.5), 0.4, 36.0, 0.1),
        ]

    def update_positions(self):
        for planet in self.planets:
            planet.update_position()

    def draw(self):
        for planet in self.planets:
            planet.draw()


def draw_stars():
    glPointSize(1.5)
    glBegin(GL_POINTS)
    for _ in range(100):
        glColor3f(np.random.uniform(0.0, 1.0), np.random.uniform(0.0, 1.0), np.random.uniform(0.0, 1.0))
        glVertex3f(np.random.uniform(-30.0, 30.0), np.random.uniform(-30.0, 30.0), np.random.uniform(-30.0, 30.0))
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(500, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

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
