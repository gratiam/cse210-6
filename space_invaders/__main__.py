import os
import random

from game.casting.actor import Actor
from game.casting.invader import Invader
from game.casting.cast import Cast

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point
from constants import *

## TODO: make game over stop the game
def main():
    # create the cast
    cast = Cast()
    
    # create the HUD
    score = Actor()
    score.set_text("Score: 0")
    score.set_font_size(FONT_SIZE)
    score.set_color(WHITE)
    score.set_position(Point(int(MAX_X/2), 0))
    cast.add_actor("banners", score)

    # create the ship
    # x = int(MAX_X / 2)
    # y = int(MAX_Y / 1.1)
    x = 15
    y = 18
    position = Point(x, y)
    position = position.scale(CELL_SIZE)
    ship = Actor()
    ship.set_text("^")
    ship.set_font_size(FONT_SIZE)
    ship.set_color(GREEN)
    ship.set_position(position)
    cast.add_actor("ships", ship)

    

    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()