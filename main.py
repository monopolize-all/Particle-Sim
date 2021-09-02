from preferences import *

import pyglet
import json

import particles


window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

fps_display = pyglet.window.FPSDisplay(window)

grid = [[None for y in range(GRID_ROWS)] for x in range(GRID_COLS)]

particles_display_batch = pyglet.graphics.Batch()


def add_particle_to_grid(particle_class, grid_x, grid_y):

    pos_x = GRID_OFFSET_HORIZONTAL + GRID_PADDING_HORIZONTAL + grid_x * (PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL)
    pos_y = GRID_OFFSET_VERTICAL + GRID_PADDING_VERTICAL + grid_y * (PARTICLE_HEIGHT + GRID_SPACING_VERTICAL)

    if grid[grid_x][grid_y] is None:

        colour = particle_class.BASE_COLOUR
        sprite = pyglet.shapes.Rectangle(pos_x, pos_y, PARTICLE_WIDTH, PARTICLE_HEIGHT, color = colour, batch = particles_display_batch)
        position = grid_x, grid_y
        particle = particle_class(grid, sprite, position)

        grid[grid_x][grid_y] = particle


def update_particles(dt):
    for col in grid:
        for particle in col:
            if particle is not None:
                particle.update(dt)

pyglet.clock.schedule_interval(update_particles, 1 / FPS)

@window.event       
def on_mouse_press(x, y, button, modifiers):
    x -= GRID_OFFSET_HORIZONTAL + GRID_PADDING_HORIZONTAL
    y -= GRID_OFFSET_VERTICAL + GRID_PADDING_VERTICAL

    if not (x >= 0 and y >= 0):
        return
        
    if not x < GRID_COLS * (PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL):
        return

    if not y < GRID_ROWS * (PARTICLE_HEIGHT + GRID_SPACING_VERTICAL):
        return

    grid_x = x // (PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL)
    grid_y = y // (PARTICLE_HEIGHT + GRID_SPACING_VERTICAL)

    if button == pyglet.window.mouse.LEFT:

        particle_class = particles.fluid.Fluid
        add_particle_to_grid(particle_class, grid_x, grid_y)

    elif button == pyglet.window.mouse.RIGHT:
        if grid[grid_x][grid_y] is not None:
            grid[grid_x][grid_y].delete()
  

@window.event
def on_draw():
    window.clear()

    particles_display_batch.draw()

    if SHOW_FPS:
        fps_display.draw()


pyglet.app.run()
