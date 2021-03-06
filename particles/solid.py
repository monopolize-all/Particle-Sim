import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from preferences import *


class Solid:

    BASE_COLOUR = (205, 185, 156)
    MASS = 1
    PHYSICS_ENABLED = True

    def __init__(self, grid, sprite, position):
        self.grid = grid
        self.sprite = sprite
        self.gx, self.gy = position

        self.grid.add_to_updates(self)

        if self.PHYSICS_ENABLED:
            self.x = 0.5
            self.y = 0.5
            self.vx = self.vy = 0
            self.ax = self.ay = 0

    def delete(self):
        self.sprite.delete()
        self.grid[self.gx, self.gy] = None

    def update(self, dt):
        update_is_required = False

        if self.PHYSICS_ENABLED:
            self.update_kinematics(dt)
            update_is_required = True

        return update_is_required
        
    def update_kinematics(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Gravitational forces
        if GRAVITATIONAL_FORCES_ENABLED and self.MASS:
            self.vx += GRAVITY_FORCE_HORIZONTAL * dt
            self.vy += GRAVITY_FORCE_VERTICAL * dt

        if self.x > 1:
            if self.gx < GRID_COLS - 1 and self.grid[self.gx + 1, self.gy] is None:
                self.grid[self.gx, self.gy] = None

                self.gx += 1
                self.x = 0
                self.sprite.x += PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL

                self.grid[self.gx, self.gy] = self
            
            else:
                self.x = 1
                self.vx = 0

        elif self.x < 0:
            if self.gx > 0 and self.grid[self.gx - 1, self.gy] is None:
                self.grid[self.gx, self.gy] = None

                self.gx -= 1
                self.x = 1
                self.sprite.x -= PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL

                self.grid[self.gx, self.gy] = self

            else:
                self.x = 0
                self.vx = 0

        if self.y > 1:
            if self.gy < GRID_ROWS - 1 and self.grid[self.gx, self.gy + 1] is None:
                self.grid[self.gx, self.gy] = None

                self.gy += 1
                self.y = 0
                self.sprite.y += PARTICLE_HEIGHT + GRID_SPACING_VERTICAL

                self.grid[self.gx, self.gy] = self

            else:
                self.y = 1
                self.vy = 0

        elif self.y < 0:
            if self.gy > 0 and self.grid[self.gx, self.gy - 1] is None:
                self.grid[self.gx, self.gy] = None

                self.gy -= 1
                self.y = 1
                self.sprite.y -= PARTICLE_HEIGHT + GRID_SPACING_VERTICAL

                self.grid[self.gx, self.gy] = self

            else:
                self.y = 0
                self.vy = 0
