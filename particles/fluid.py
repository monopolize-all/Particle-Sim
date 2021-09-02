import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from preferences import *


class Fluid:

    BASE_COLOUR = (0, 117, 119)
    MASS = 1

    def __init__(self, grid, sprite, position):
        self.grid = grid
        self.sprite = sprite
        self.gx, self.gy = position

        self.x = PARTICLE_WIDTH // 2
        self.y = PARTICLE_HEIGHT // 2
        self.vx = self.vy = 0
        self.ax = self.ay = 0

    def update(self, dt):
        self.update_kinematics(dt)
        
    def update_kinematics(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # GRAVITY
        self.vy -= 100 * dt

        if self.x > PARTICLE_WIDTH:
            if self.gx < GRID_COLS - 1 and self.grid[self.gx + 1][self.gy] is None:
                self.grid[self.gx][self.gy] = None

                self.gx += 1
                self.x = 0
                self.sprite.x += PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL

                self.grid[self.gx][self.gy] = self
            
            else:
                self.x = PARTICLE_WIDTH

        elif self.x < 0:
            if self.gx > 0 and self.grid[self.gx - 1][self.gy] is None:
                self.grid[self.gx][self.gy] = None

                self.gx -= 1
                self.x = PARTICLE_WIDTH
                self.sprite.x -= PARTICLE_WIDTH + GRID_SPACING_HORIZONTAL

                self.grid[self.gx][self.gy] = self

            else:
                self.x = 0

        if self.y > PARTICLE_HEIGHT:
            if self.gy < GRID_ROWS - 1 and self.grid[self.gx][self.gy + 1] is None:
                self.grid[self.gx][self.gy] = None

                self.gy += 1
                self.y = 0
                self.sprite.y += PARTICLE_HEIGHT + GRID_SPACING_VERTICAL

                self.grid[self.gx][self.gy] = self

            else:
                self.y = PARTICLE_HEIGHT

        elif self.y < 0:
            if self.gy > 0 and self.grid[self.gx][self.gy - 1] is None:
                self.grid[self.gx][self.gy] = None

                self.gy -= 1
                self.y = PARTICLE_HEIGHT
                self.sprite.y -= PARTICLE_HEIGHT + GRID_SPACING_VERTICAL

                self.grid[self.gx][self.gy] = self

            else:
                self.y = 0