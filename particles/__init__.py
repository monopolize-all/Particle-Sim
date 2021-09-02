from .solid import Solid
from .fluid import Fluid

particles = [Solid, Fluid]
number_of_particles = len(particles)
current_particle_index = 0

def get_current_particle():
    return particles[current_particle_index]

get_current_particle()
