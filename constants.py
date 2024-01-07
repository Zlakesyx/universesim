import pygame

WIDTH = 1280
HEIGHT = 720

# TODO Not a fan of this implementation as it creates a screen once this file
# is imported
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# F = ma = d/dt(mv)
# F = G * (M1 * M2) / r^2
AU = 1.495978707e11  # meters
G = 6.67430e-11
SCALE = 100 / AU
TIMESTEP = 86400  # 60s * 60m = 3600s/h * 24h = 86400s/day

"""
F = ma = d/dt(mv)
m = 10 kg
v = 40 m/s
a = 400 kgm/s)
"""
