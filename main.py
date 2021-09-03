# region import
from preferences import *

import pyglet

import particles
# endregion

# region misc
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

fps_display = pyglet.window.FPSDisplay(window)

ui_batch = pyglet.graphics.Batch()
ui_elements = []
# endregion

# region grid
class Grid:
    
    def __init__(self):
        self.matrix = [[None for y in range(GRID_ROWS)] for x in range(GRID_COLS)]

        self.display_batch = pyglet.graphics.Batch()

        self.add_borders()

    def add_borders(self):
        x1 = GRID_OFFSET_HORIZONTAL
        y1 = GRID_OFFSET_VERTICAL
        x2 = GRID_OFFSET_HORIZONTAL + GRID_WIDTH
        y2 = GRID_OFFSET_VERTICAL + GRID_HEIGHT

        ui_elements.append(pyglet.shapes.Line(x1, y1, x2, y1, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))
        
        ui_elements.append(pyglet.shapes.Line(x1, y1, x1, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        ui_elements.append(pyglet.shapes.Line(x2, y1, x2, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        ui_elements.append(pyglet.shapes.Line(x1, y2, x2, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

    def __setitem__(self, key, value):
        x, y = key
        self.matrix[x][y] = value

    def __getitem__(self, key):
        x, y = key
        return self.matrix[x][y]

    def __iter__(self):
        for column in self.matrix:
            for particle in column:
                yield particle

grid = Grid()
# endregion

# region particle selection menu
class Particle_Selection_Menu:

    def __init__(self):
        self.menus = []
        self.scrolled_value = 0
        self.scrolled_index = 0

        self.add_particle_menus()

        self.add_borders()

        self.on_scroll(0, 0, 0)

    def add_particle_menus(self):
        selected_menu_horizontal_position = PARTICLE_SELECTION_MENU_POSITION_HORIZONTAL + PARTICLE_SELECTION_MENU_PADDING_HORIZONTAL
        selected_menu_vertical_position = PARTICLE_SELECTION_MENU_POSITION_VERTICAL + (PARTICLE_SELECTION_MENU_HEIGHT - PARTICLE_SELECTION_MENU_PARTICLE_HEIGHT) // 2
        self.particle_menu_vertical_step = PARTICLE_SELECTION_MENU_PARTICLE_HEIGHT + PARTICLE_SELECTION_MENU_PADDING_VERTICAL
        
        for particle_list in particles.particles:
            particle = particle_list[0]
            particle_name = particle.__name__
            particle_colour = particle.BASE_COLOUR

            sprite = pyglet.shapes.Rectangle(selected_menu_horizontal_position, 
                                            selected_menu_vertical_position, 
                                            PARTICLE_SELECTION_MENU_PARTICLE_WIDTH, 
                                            PARTICLE_SELECTION_MENU_PARTICLE_HEIGHT, 
                                            color = particle_colour, batch = grid.display_batch)

            selected_menu_vertical_position += self.particle_menu_vertical_step

            menu_entry = sprite, particle_name, particle_colour, particle_list

            self.menus.append(menu_entry)

    def add_borders(self):
        x1 = PARTICLE_SELECTION_MENU_POSITION_HORIZONTAL
        y1 = PARTICLE_SELECTION_MENU_POSITION_VERTICAL
        x2 = PARTICLE_SELECTION_MENU_POSITION_HORIZONTAL + PARTICLE_SELECTION_MENU_WIDTH
        y2 = PARTICLE_SELECTION_MENU_POSITION_VERTICAL + PARTICLE_SELECTION_MENU_HEIGHT

        ui_elements.append(pyglet.shapes.Line(x1, y1, x2, y1, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))
        
        ui_elements.append(pyglet.shapes.Line(x1, y1, x1, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        ui_elements.append(pyglet.shapes.Line(x2, y1, x2, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        ui_elements.append(pyglet.shapes.Line(x1, y2, x2, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        self.bounding_box = (x1, y1, x2, y2)

        x1 = PARTICLE_SELECTION_MENU_POSITION_HORIZONTAL + PARTICLE_SELECTION_MENU_PADDING_HORIZONTAL
        y1 = PARTICLE_SELECTION_MENU_POSITION_VERTICAL + (PARTICLE_SELECTION_MENU_HEIGHT - PARTICLE_SELECTION_MENU_PARTICLE_HEIGHT) // 2 - 1
        x2 = x1 + PARTICLE_SELECTION_MENU_PARTICLE_WIDTH + 1
        y2 = y1 + PARTICLE_SELECTION_MENU_PARTICLE_HEIGHT + 1

        ui_elements.append(pyglet.shapes.Line(x1, y1, x2, y1, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))
        
        ui_elements.append(pyglet.shapes.Line(x1, y1, x1, y2 + 1, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        ui_elements.append(pyglet.shapes.Line(x2, y1, x2, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        ui_elements.append(pyglet.shapes.Line(x1, y2, x2, y2, width = 1, 
                                        color = UI_BORDER_COLOUR, batch = ui_batch))

        self.current_particle_menu_bounding_box = (x1, y1, x2, y2)
    
    def draw(self):
        for sprite in self.menus:
            sprite[0].draw()

    def on_scroll(self, scroll, x, y):
        self.scrolled_value += scroll * PARTICLE_SELECTION_MENU_SCROLL_SENSITIVITY
        self.scrolled_value = max(self.scrolled_value, 0)
        self.scrolled_value = min(self.scrolled_value, len(self.menus) - 1)
        
        new_scrolled_index = int(self.scrolled_value)

        step = self.scrolled_index - new_scrolled_index

        for menu in self.menus:
            menu[0].y += self.particle_menu_vertical_step * step

        self.scrolled_index = new_scrolled_index

        particles.currently_selected_particle = self.menus[self.scrolled_index][3][0]

        x1, y1, x2, y2 = self.current_particle_menu_bounding_box
        if x1 < x < x2 and y1 < y < y2:
            self.on_mouse_over_current_menu()

    def on_mouse_over_current_menu(self):
        pass

particle_selection_menu = Particle_Selection_Menu()

# endregion
 
# region custom functions
def add_particle_to_grid(particle_class, grid_x, grid_y):

    pos_x = GRID_OFFSET_HORIZONTAL + GRID_PADDING_HORIZONTAL + PARTICLE_OFFSET_HORIZONTAL + grid_x * (PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL)
    pos_y = GRID_OFFSET_VERTICAL + GRID_PADDING_VERTICAL + PARTICLE_OFFSET_VERTICAL + grid_y * (PARTICLE_HEIGHT + GRID_SPACING_VERTICAL)

    if grid[grid_x, grid_y] is None:

        colour = particle_class.BASE_COLOUR
        sprite = pyglet.shapes.Rectangle(pos_x, pos_y, PARTICLE_WIDTH, PARTICLE_HEIGHT, color = colour, batch = grid.display_batch)
        position = grid_x, grid_y
        particle = particle_class(grid, sprite, position)

        grid[grid_x, grid_y] = particle


def update_particles(dt):
    for particle in grid:
        if particle is not None:
            particle.update(dt)

pyglet.clock.schedule_interval(update_particles, 1 / FPS)
# endregion

# region window events
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

        particle_class = particles.currently_selected_particle
        add_particle_to_grid(particle_class, grid_x, grid_y)

    elif button == pyglet.window.mouse.RIGHT:
        if grid[grid_x, grid_y] is not None:
            grid[grid_x, grid_y].delete()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    x1, y1, x2, y2 = particle_selection_menu.bounding_box
    if x1 < x < x2 and y1 < y < y2:
        particle_selection_menu.on_scroll(scroll_y, x, y)

@window.event
def on_mouse_motion(x, y, dx, dy):
    x1, y1, x2, y2 = particle_selection_menu.current_particle_menu_bounding_box
    if x1 < x < x2 and y1 < y < y2:
        particle_selection_menu.on_mouse_over_current_menu()

@window.event
def on_draw():
    window.clear()

    grid.display_batch.draw()

    ui_batch.draw()

    particle_selection_menu.draw()

    if SHOW_FPS:
        fps_display.draw()
# endregion

pyglet.app.run()
