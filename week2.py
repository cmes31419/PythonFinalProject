"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import math
import random
from typing import List

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util


class BouncyBalls(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    def __init__(self) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 0.0)

        self._screen_width = 600
        self._screen_height = 600

        self._direction = math.pi/360

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Balls that exist in the world
        self._balls: List[pymunk.Circle] = []

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        self._create_arrow()
        for i in range(5):
            self._create_ball(x=random.randint(25, 600-25), y=random.randint(25, 600-25))
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._update()
            self._process_events()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(50)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [    # 設置牆壁範圍
            pymunk.Segment(static_body, (0.0, 0.0), (0.0, self._screen_height), 0.0),
            pymunk.Segment(static_body, (0.0, self._screen_height), (self._screen_width, self._screen_height), 0.0),
            pymunk.Segment(static_body, (self._screen_width, self._screen_height), (self._screen_width, 0.0), 0.0),
            pymunk.Segment(static_body, (self._screen_width, 0.0), (0.0, 0.0), 0.0),
        ]
        for line in static_lines:
            line.elasticity = 0.1
            line.friction = 1.0
        self._space.add(*static_lines)

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # 按P擷取遊戲畫面
                pygame.image.save(self._screen, "balls_and_arrow.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 按空白鍵發射
                Vx = 1200*math.cos(self._direction)
                Vy = -1200*abs(math.sin(self._direction))
                self._create_ball(x=300, y=600, Vx=Vx, Vy=Vy)

    def _update(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        #self._ticks_to_next_ball -= 1
        #if self._ticks_to_next_ball <= 0:
            #self._create_ball()
            #self._ticks_to_next_ball = 100
        self._direction += math.pi/180  # 發射角度隨時間改變
        if self._direction > 2*math.pi:
            self._direction -= 2*math.pi
        self._arrow_body.angle = -self._direction if self._direction < math.pi else self._direction 
        # Remove balls that fall below 100 vertically
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 600]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def _create_arrow(self):   # 方向標
        vs = [(-10, 0), (0, 3), (50, 0), (0, -3)]   # 方向標形狀
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        shape = pymunk.Poly(body, vs)
        body.position = 300, 600
        body.angle = self._direction
        self._space.add(body, shape)
        self._arrow_body = body

    def _create_ball(self, x, y, Vx=0, Vy=0) -> None:
        """
        Create a ball.
        :return:
        """
        mass = 10
        radius = 15
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        #x = random.randint(25, 600-25)
        #y = random.randint(25, 600-25)
        body.position = x, y
        body.velocity = Vx, Vy
        body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, (0,0), 0.98, self._dt)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.1
        shape.friction = 1.0
        self._space.add(body, shape)
        self._balls.append(shape)

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)


game = BouncyBalls()
game.run()
