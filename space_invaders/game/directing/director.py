from random import randint
from game.shared.point import Point
from game.casting.invader import Invader
from game.casting.actor import Actor
from game.casting.cast import Cast
from game.casting.bullet import Bullet
from constants import *
import pyray

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        self._game_over = False
        self._game_ended = False
        self._game_tick = 0
        self._invader_direction = "left"
        self._lives = LIVES

    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        # create life hud
        lives = Actor()
        lives.set_text(f"Lives: {'O'*self._lives}")
        lives.set_font_size(FONT_SIZE)
        lives.set_color(GREEN)
        lives.set_position(Point(CELL_SIZE, 0))
        cast.add_actor("banners", lives)

        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)

            # if game is over
            if not self._game_ended and self._game_over:
                self._handle_gameover(cast)

        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        ship = cast.get_first_actor("ships")
        velocity = self._keyboard_service.get_direction()
        ship.set_velocity(velocity)
        
        # if the space key is being pressed
        bullet_fired = self._keyboard_service.key_pressed(pyray.KEY_SPACE)
        if (bullet_fired and len(cast.get_actors("bullets")) == 0) and not self._game_ended:
            # create new bullet
            bullet = Bullet()
            position = ship.get_position()
            bullet.set_position(position)
            bullet.set_color(ship.get_color())
            bullet.set_text("|")
            cast.add_actor("bullets", bullet)
            # set velocity upwards
        try:
            bullet.set_velocity(Point(0, CELL_SIZE*-1))
        except UnboundLocalError: pass

    def _do_updates(self, cast):
        """Updates the ship's position and resolves any collisions with invaders.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banners = cast.get_actors("banners")
        ship = cast.get_first_actor("ships")
        invaders = cast.get_actors("invaders")

        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        ship.move_next(max_x, max_y)
        
        self._game_tick += 1
        if self._game_tick > 20: self._game_tick = 0
        
        # bullet
        bullet = cast.get_first_actor("bullets")
        if bullet != None:
            bullet.move_next(max_x, max_y)

            # if bullet left screen
            if bullet.get_position().get_y() < 1:
                # remove bullet
                cast.remove_actor("bullets", bullet)
            # if bullet on screen
            else:
                # for every invader
                for invader in invaders:
                    # if bullet hit invader
                    if bullet.get_position().scale(CELL_SIZE).approx_equals(invader.get_position().scale(CELL_SIZE)):
                        # remove invader and bullet
                        print("Bullet hit invader")
                        cast.remove_actor("invaders", invader)
                        cast.remove_actor("bullets", bullet)
                        # update score
                        self._score += 10
                        banners[0].set_text(f"Score: {self._score}")
                        break

        

        # spawn new invaders if all have been destroyed
        invader = Invader()
        invader.spawn_invaders(cast, 20)

        
        # move the space invaders
        self._move_invaders(cast)

        # end game/lose life if an invader has left screen
        for invader in invaders:
            # remove Invader if it has left the screen
            if invader.get_position().y_greater_than(600):
                cast.remove_actor("invaders", invader)
                self._lives -= 1
                banners[1].set_text(f"Lives: {'O'*self._lives}")
                if self._lives == 0:
                    self._game_over = True

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()

    def _handle_gameover(self, cast):
        x = int(MAX_X / 2)
        y = int(MAX_Y / 2)
        position = Point(x, y)

        message = Actor()
        message.set_text("GAME OVER")
        message.set_font_size(FONT_SIZE)
        message.set_color(RED)
        message.set_position(position)
        cast.add_actor("messages", message)
        # change ship to red
        
        ship = cast.get_first_actor("ships")
        ship.set_color(RED)
        self._game_ended = True

        
        
    def _move_invaders(self, cast):
        """Move the space invader group."""
        # if game tick is even
        if self._game_tick % 2 == 0:
            invaders = cast.get_actors("invaders")
            # reset additional values
            add_y = 0
            add_x = 0
            # if possition is right
            if self._invader_direction == "right":
                # set x to add 1
                add_x = 1
                # if invader about to leave right side of screen
                if invaders[-1].get_position().get_x()+30 >= MAX_X:
                    print("Hit right of screen")
                    # change direction
                    self._invader_direction = "left"
                    # subract 1
                    add_x = -1
                    # add one
                    add_y = 1
            
            elif self._invader_direction == "left": 
                add_x = -1
                # if invader about to leave left side of screen
                if invaders[0].get_position().get_x()-CELL_SIZE <= 1:
                    print("Hit left of screen")
                    # change direction
                    self._invader_direction = "right"
                    add_x = 1
                    add_y = 1
            else: print("None")

            for invader in invaders:
                # move x and y
                x = invader.get_position().get_x()+(add_x*CELL_SIZE)
                y = invader.get_position().get_y()+(add_y*CELL_SIZE)
                invader.set_position(Point(x, y))
