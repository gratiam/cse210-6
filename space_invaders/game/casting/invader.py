from constants import *
from game.casting.actor import Actor
from game.shared.point import Point
from game.shared.color import Color
import random
class Invader(Actor):
    """A Space Invader.  The job of the Invader is to create itself."""
    def __init__(self):
        # carries over actor attributes
        super().__init__()

    def spawn_invaders(self, cast, number):
        """Creates a number of invaders on the top of the screen
        Args:
            cast (Class): the cast lets us add new actors.
            number (int): the number of invaders there should be total on the screen.
        """
        ## Invader to test game over
        # invader = Invader()
        # invader.set_text("#")
        # invader.set_font_size(FONT_SIZE)
        # invader.set_color(Color(255, 255, 255))
        # invader.set_position(Point(int(MAX_X / 2), MAX_Y))
        # cast.add_actor("invaders", invader)

        # if there are no more invaders
        # if len(cast.get_actors("invaders")) == 0:
        #     # spawn new invaders
        #     # formation 1
        #     # rows
        #     for i in range(-5, 0):
        #         # columns
        #         for j in range(10, 20, 2):
        #             self._create_invader(cast, j, i)
        
        if len(cast.get_actors("invaders")) == 0:
            # spawn new invaders
            # formation 1
            # columns
            for i in range(10, 20, 2):
                # rows
                for j in range(-3, 0):
                    self._create_invader(cast, i, j)
    

    def _create_invader(self, cast, x, y):
        """Creates a space invader at desired location.
        
        args:
            cast (Class): the cast lets us add new actors.
            x (int): the column.
            y (int): the row.
        """
        position = Point(x, y)
        position = position.scale(CELL_SIZE)
        color = WHITE
        invader = Invader()
        invader.set_text("#")
        invader.set_font_size(FONT_SIZE)
        invader.set_color(color)
        invader.set_position(position)
        cast.add_actor("invaders", invader)