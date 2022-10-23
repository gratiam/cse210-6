import pyray
from game.shared.point import Point


class KeyboardService:
    """Detects player input. 
    
    The responsibility of a KeyboardService is to detect player key presses and translate them into 
    a point representing a direction.

    Attributes:
        cell_size (int): For scaling directional input to a grid.
    """

    def __init__(self, cell_size = 1):
        """Constructs a new KeyboardService using the specified cell size.
        
        Args:
            cell_size (int): The size of a cell in the display grid.
        """
        self._cell_size = cell_size

    def get_direction(self):
        """Gets the selected direction based on the currently pressed keys.

        Returns:
            Point: The selected direction.
        """
        dx = 0
        dy = 0

        if pyray.is_key_down(pyray.KEY_LEFT) or pyray.is_key_down(pyray.KEY_A):
            dx = -1
        
        if pyray.is_key_down(pyray.KEY_RIGHT) or pyray.is_key_down(pyray.KEY_D):
            dx = 1
        
        # up and down
        # if pyray.is_key_down(pyray.KEY_UP):
        #     dy = -1
        
        # if pyray.is_key_down(pyray.KEY_DOWN):
        #     dy = 1

        direction = Point(dx, dy)
        direction = direction.scale(self._cell_size)
        
        return direction
    def key_pressed(self, key):
        """returns True if selected key is pressed, otherwise returns False.
        Args:
            key (int): a pyray key should be chosen here, e.g. pyray.KEY_SPACE
        """
        if pyray.is_key_down(key):
            return True
        else: False