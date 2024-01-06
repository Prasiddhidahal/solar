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

    # method to draw planets and its axis of rotation
    def draw(self):
        # Draw 2D orbit path
        num_segments = 100  # Number of line segments to create a smooth orbit
        glColor3f(0.5, 0.5, 0.5)  # Set the color for the orbit (gray)
        glBegin(GL_LINE_LOOP)  # Begin drawing line loop for the orbit
        for i in range(num_segments):
            angle = 2.0 * math.pi * float(i) / num_segments  # Calculate the angle for each segment
            x = math.cos(angle) * self.distance  # Calculate the x-coordinate of the point on the orbit
            y = math.sin(angle) * self.distance  # Calculate the y-coordinate of the point on the orbit
            glVertex3f(x, y, 0.0)  # Specify the vertex position for the point on the orbit
        glEnd()  # End drawing the orbit

        # Draw planet
        glPushMatrix()  # Push the current matrix onto the stack
        glColor3f(self.color[0], self.color[1], self.color[2])  # Set the color for the planet
        glRotatef(self.angle, 0.0, 0.0, 1.0)  # Apply rotation around the z-axis using the current angle
        glTranslatef(self.distance, 0.0, 0.0)  # Apply translation along the x-axis to position the planet
        glBegin(GL_TRIANGLE_FAN)  # Begin drawing triangle fan for the planet
        glVertex3f(0.0, 0.0, 0.0)  # Specify the vertex position for the center of the planet
        for i in range(num_segments + 1):
            angle = 2.0 * math.pi * float(i) / num_segments  # Calculate the angle for each segment. evenly distributes the vertices around the circle by dividing the full circle (2π radians) into num_segments equal parts.
            x = math.sin(angle) * self.radius  # Calculate the x-coordinate of the point on the planet's circumference, , Multiplying it by the radius gives the actual x-coordinate.
            y = math.cos(angle) * self.radius  # Calculate the y-coordinate of the point on the planet's circumference
            glVertex3f(x, y, 0.0)  # Specify the vertex position for a point on the planet's circumference
        glEnd()  # End drawing the planet
        glPopMatrix()  # Pop the matrix from the stack, restoring the previous matrix state

    def update_position(self):
    # Update the angle of the planet's position based on its speed for each frame or iteration in the simulation.
        self.angle += self.speed


def update_planet_positions(planets):
    for planet in planets:
        planet.update_position()


def draw_stars():
    glPointSize(4.0)  # Set a larger size for the stars
    glBegin(GL_POINTS)  # Start drawing stars
    num_stars = 100  # Number of stars to draw

    for _ in range(num_stars):
        r, g, b = np.random.uniform(0.0, 1.0, size=3)  # Random RGB values for star color
        glColor3f(r, g, b)  # Set the color for the star
        # Generate random star positions in the range [-20, 20]
        x = np.random.uniform(-30.0, 30.0)
        y = np.random.uniform(-30.0, 30.0)
        z = np.random.uniform(-30.0, 30.0)
        glVertex3f(x, y, z)  # Draw a star at the generated position

    glEnd()  # End drawing stars

def main():
    planets = [
    Planet("Sun", (1.0, 1.0, 0.0), 2.2, 0.0, 0.0),  # Yellow color for the Sun
    Planet("Mercury", (0.7, 0.7, 0.7), 0.3, 4.0, 0.9),  # Gray color for Mercury
    Planet("Venus", (0.8, 0.5, 0.0), 0.6, 8.0, 0.8),  # Orange-like color for Venus
    Planet("Earth", (0.0, 0.0, 1.0), 0.9, 12.0, 0.7),  # Blue color for Earth
    Planet("Mars", (1.0, 0.0, 0.0), 0.45, 16.0, 0.6),  # Red color for Mars
    Planet("Jupiter", (0.9, 0.6, 0.0), 2, 20.0, 0.5),  # Orange color for Jupiter
    Planet("Saturn", (1,0.5, 0), 2.5, 24.0, 0.4),
    Planet("Uranus", (0.0, 0.5, 0.5), 2.4, 28.0, 0.3),  # Blue-green color for Uranus
    Planet("Neptune", (0.4, 0.5, 0.5), 2.1, 32.0, 0.2),
    Planet("Pluto", (0.5, 0.5, 0.5), 0.4, 36.0, 0.1),
    
]

    pygame.init()
    display = (1800, 700)  # width, height of the display window
    pygame.display.set_caption('The Solar System Simulation')
    # Set up the Pygame window mode for OpenGL rendering.
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    # Set the perspective projection for the 3D scene.
    # Parameters: field of view angle, aspect ratio, near clipping plane, far clipping plane.
    gluPerspective(80, (display[0] / display[1]), 0.1, 50.0)

    # Apply a translation to the entire scene to move it along the z-axis.
    # Parameters: x-axis translation, y-axis translation, z-axis translation.
    glTranslatef(0.0, 0.0, -20.0)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Clear the color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the stars
        draw_stars()

        # Update the positions of the planets.
        update_planet_positions(planets)

        # Draw each planet in the scene.
        for planet in planets:
            planet.draw()

        # Flip the display to update the screen.
        pygame.display.flip()

        # Add a small delay to control the frame rate.
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
#add resolution and make stars 

 
