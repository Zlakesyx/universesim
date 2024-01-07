import math
import pygame
import constants as const


class CelestialBody:
    def __init__(
        self,
        mass: float,
        radius: float,
        x: float,
        y: float,
        name: str,
        x_velocity: float = 0,
        y_velocity: float = 0,
        color: pygame.Color = None
    ) -> None:
        self.mass = float(mass)
        self.radius = float(radius)
        self.x = float(x)
        self.y = float(y)
        self.x_velocity = float(x_velocity)
        self.y_velocity = float(y_velocity)
        self.name = name
        self.collided_body = None

        if color:
            self.color = color
        else:
            self.color = "gray"

    def update(self, celestial_bodies: dict) -> None:
        total_force_x = 0
        total_force_y = 0

        for body_type in celestial_bodies:
            for other_body in celestial_bodies[body_type]:
                if other_body is self:
                    continue

                x_dist = other_body.x - self.x
                y_dist = other_body.y - self.y
                total_dist = math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))

                # check collision
                if total_dist - self.radius <= other_body.radius:
                    self.collided_body = other_body
                    other_body.collided_body = self

                theta = math.atan2(y_dist, x_dist)
                force = const.G * self.mass * other_body.mass / math.pow(total_dist, 2)  # F = GMm/r^2
                force_x = float(math.cos(theta) * force)  # cos(theta) = a/h; a = cos(theta) * h
                force_y = float(math.sin(theta) * force)  # sin(theta) = o/h; o = sin(theta) * h

                # f = m * a
                # a = f / m
                total_force_x += force_x
                total_force_y += force_y

        self.x_velocity += total_force_x / self.mass * const.TIMESTEP
        self.y_velocity += total_force_y / self.mass * const.TIMESTEP

        self.x += self.x_velocity * const.TIMESTEP
        self.y += self.y_velocity * const.TIMESTEP

    def draw(self) -> None:
        x = self.x * const.SCALE + const.WIDTH / 2
        y = self.y * const.SCALE + const.HEIGHT / 2
        pygame.draw.circle(const.SCREEN, self.color, (x, y), self.radius)


class Asteroid(CelestialBody):
    def __init__(
        self,
        mass: float,
        radius: float,
        x: float,
        y: float,
        x_velocity: float,
        y_velocity: float,
        name: str,
        color: pygame.Color = None
    ) -> None:
        self.body_type = "asteroid"
        super().__init__(mass, radius, x, y, x_velocity, y_velocity, name, color)


class Planet(CelestialBody):
    def __init__(
        self,
        mass: float,
        radius: float,
        name: str,
        color: pygame.Color = None,
        host_star: "Star" = None,
        dist_to_host: float = 0.0,
        x: float = 0.0,
        y: float = 0.0,
        x_velocity: float = 0.0,
        y_velocity: float = 0.0
    ) -> None:
        self.host_star = host_star
        self.dist_to_host = dist_to_host
        self.body_type = "planet"
        super().__init__(mass, radius, x, y, name, x_velocity, y_velocity, color)

    def set_host_star(self, star: "Star") -> None:
        self.host_star = star

    def set_pos_with_respect_to_star(self) -> None:
        if not self.dist_to_host:
            raise ValueError("dist_to_host field required")

        self.x = self.host_star.x + self.dist_to_host
        self.y = self.host_star.y


class Moon(CelestialBody):
    def __init__(
        self,
        mass: float,
        radius: float,
        name: str,
        color: pygame.Color = None,
        host_star: "Star" = None,
        host_planet: Planet = None,
        x: float = 0.0,
        y: float = 0.0,
        x_velocity: float = 0.0,
        y_velocity: float = 0.0
    ) -> None:
        self.host_star = None
        self.host_planet = None
        self.body_type = "moon"
        super().__init__(mass, radius, x, y, name, x_velocity, y_velocity, color)

    def set_host_star(self, star: "Star") -> None:
        self.host_star = star

    def set_host_planet(self, planet: Planet) -> None:
        self.host_planet = planet

    def set_pos_with_respect_to_planet(self, x: float, y: float) -> None:
        self.x = self.host_planet.x + x
        self.y = self.host_planet.y + y


class Star(CelestialBody):
    def __init__(
        self,
        mass: float,
        radius: float,
        x: float,
        y: float,
        name: str,
        color: pygame.Color = None,
        planets: list[Planet] = None
    ) -> None:
        self.planets = planets
        self.body_type = "star"
        super().__init__(mass, radius, x, y, name, color=color)
