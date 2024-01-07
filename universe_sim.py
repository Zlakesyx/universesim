import random
import pygame

import constants as const
from celestial_body import Planet, Star


class UniverseSim:

    def __init__(self):
        pygame.init()

        self.running = True
        self.planets = []
        self.stars = []
        self.asteroids = []
        self.moons = []
        self.celestial_bodies = {
                "planet": self.planets,
                "star": self.stars,
                "asteroid": self.asteroids,
                "moon": self.moons
         }
        self.planet_counter = 0
        self.year = 0
        self.day = 1

        self.new_game()

    def update(self) -> None:
        for body_type in self.celestial_bodies:
            for r_index, body in enumerate(reversed(self.celestial_bodies[body_type])):
                body.update(self.celestial_bodies)

                if body.collided_body:
                    index_length = len(self.celestial_bodies[body_type]) - 1
                    if body.mass < body.collided_body.mass:
                        self.celestial_bodies[body_type].pop(index_length - r_index)
                        body.collided_body.mass += body.mass
                        body.collided_body.radius += body.radius / 4
                        body.collided_body.collided_body = None
                    else:
                        self.celestial_bodies[body.collided_body.body_type].remove(body.collided_body)
                        body.mass += body.collided_body.mass
                        body.radius += body.collided_body.radius / 4
                        body.collided_body = None

    def render(self) -> None:
        const.SCREEN.fill((20, 5, 30))
        for body_type in self.celestial_bodies:
            for body in self.celestial_bodies[body_type]:
                body.draw()

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("Restarting game...")
                    self.new_game()
                elif event.key == pygame.K_q:
                    print("Exiting game...")
                    self.running = False
                elif event.key == pygame.K_p:
                    print("Spawning planet...")
                    self.planet_counter += 1
                    mass = random.randint(3e23, 3e25)
                    #mass = 4.297e9 * self.stars[0].mass
                    dist_to_host = random.uniform(0, 4) * const.AU
                    planet = Planet(
                        mass=mass,
                        radius=5,
                        name=f"p-{self.planet_counter}",
                        host_star=self.stars[0],
                        dist_to_host=dist_to_host,
                        y_velocity=random.randint(20e3, 45e3)
                    )
                    planet.set_pos_with_respect_to_star()
                    self.planets.append(planet)

    def update_time(self) -> None:
        days_in_year = 365

        print(f"Year: {self.year}, Day: {self.day}")

        if self.day % days_in_year == 0:
            self.year += 1
            self.day = 0

        self.day += 1

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            self.update_time()
            self.check_events()
            self.update()
            self.render()

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def new_game(self) -> None:
        self.planets = []
        self.stars = []
        self.asteroids = []
        self.moons = []
        self.planet_counter = 0
        self.year = 0
        self.day = 1
        self.planets = [
            Planet(mass=3.285e23, radius=1, name="Mercury", color="grey", dist_to_host=0.4 * const.AU, y_velocity=-47e3),
            Planet(mass=4.867e24, radius=2.8, name="Venus", color="orange", dist_to_host=0.72 * const.AU, y_velocity=35e3),
            Planet(mass=5.972e24, radius=3, name="Earth", color="blue", dist_to_host=1 * const.AU, y_velocity=29.784e3),
            Planet(mass=6.417e23, radius=1.5, name="Mars", color="red", dist_to_host=1.5 * const.AU, y_velocity=24.1e3),
            Planet(mass=18.98e26, radius=7, name="Jupiter", color="brown", dist_to_host=5.2 * const.AU, y_velocity=13.1e3)
        ]
        self.stars = [
            Star(mass=1.9882e30, radius=15, x=0, y=0, name="Sun", color="yellow", planets=self.planets)
        ]

        for planet in self.planets:
            planet.set_host_star(self.stars[0])
            planet.set_pos_with_respect_to_star()

        self.celestial_bodies.update(
            {
                "planet": self.planets,
                "star": self.stars,
                "asteroid": self.asteroids,
                "moon": self.moons
            }
        )


def main() -> None:
    sim = UniverseSim()
    sim.run()


if __name__ == "__main__":
    main()
