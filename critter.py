"""
Author: TBSDrJ
Date: Fall 2024
Purpose: Provides:
   1. A base class that each student's custom critter class can inherit from.
   2. A distance function
***DO NOT MODIFY THIS FILE.***
Students are expected to create their own code file, importing from this one.
"""
import random

#####
# Make sure you look at the bottom of this file for three convenience functions.
#####

class Critter:
    """Base Critter for Dr. J's Little Fantasy Combat game.
    
    Students are expected to implement/override and provide unit tests 
    for nine methods:
        - __str__() method
        - __repr__() method
        - close_attack() method
        - far_attack() method
        - move() method
        - die() method
        - close_attack_description() method
        - far_attack_description() method
        - move_description() method
    """
    total_points = 25

    def __init__(self, health: int, defense: int, close_attack_power: int, 
                far_attack_power: int, far_attack_range: int, speed: int):
        """Initialize, extensive validation of Critter stats is provided:

            - health must be at least 1.
            - defense, close_attack_power and speed must not be negative.
            - if far_attack_power is positive, then far_attack_range must 
                be at least 3.
            - if far_attack_range is positive then far_attack_power must also
                be positive.
        """
        self.health = health
        self.defense = defense
        self.close_attack_power = close_attack_power
        self.far_attack_power = far_attack_power
        self.far_attack_range = far_attack_range
        self.speed = speed

        # x, y will be non-negative integers 0 to 9, represents your location.
        # Also accessible as self.location as a pair.
        self.x = None
        self.y = None
        # Team will be 0 or 1.  If self.team == other.team, you're
        #    on the same team, if self.team != other.team, you're enemies.
        self.team = None
        # .used_attack will be set by the game engine.  True = You have 
        #    sent a .move() return value of 10 or 11 at least once this round.
        self.used_attack = False
        # .round will be set by the game engine.  This will be an integer 
        #    representing the round number in the combat.
        self.round = 0
        # .moves_completed will be set by the game engine.  This will be an
        #    an integer representing the number of moves you've already
        #    completed this round.  For example, if self.moves_completed == 
        #    self.speed, then you are on your last move.
        self.moves_completed = 0

        self.total_points = (health + defense + close_attack_power 
                + far_attack_power + far_attack_range + speed)
        if (self.total_points != __class__.total_points):
            msg = f"Total number of points must equal "
            msg += f"{__class__.total_points}.\n"
            msg += f"This call gave values: "
            msg += f"{self.health}, {self.defense}, {self.close_attack_power}, "
            msg += f"{self.far_attack_power}, {self.far_attack_range}, "
            msg += f"{self.speed}, which add to {self.total_points}\n"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Provides a human-friendly description of the critter, max 70 chars"""

    def __repr__(self) -> str:
        """Provides a string that, if executed, would create this critter"""

    def close_attack(self, *critters: "list[Critter]") -> int:
        """Decide which opponent to attack, if any in range
        
        Input critters includes all active (living) critters in
            the game, including self.
        Returns a direction to attack.  Directions match .move()
        """

    def far_attack(self, *critters: "list[Critter]") -> (int, int):
        """Decide which opponent to attack, if any in range
        
        Input critters includes all active (living) critters in
            the game, including self.
        Returns a location on the board to attack.
        """

    def move(self, *critters: "list[Critter]") -> int:
        """Decide what to do: move in some direction, attack or pass.
        
        Input critters includes all active (living) critters in
            the game, including self.
        Return:
        0 = Stand still, do not attack
        1-8 = Move, according to this diagram (x = self)
            6 7 8
            5 x 1
            4 3 2
        10 = Attack enemy that is close
            close = in one of the 8 squares that self can move to
            Must have self.close_attack_power > 0
        11 = Attack enemy that is far
            far = Must be farther away than one of the 8 squares that 
                self can move to
            Must have self.far_attack_power > 0
            distance self to enemy must be <= self.far_attack_range
        """


    def close_attack_description(self) -> str:
        """Provides a description of what this critter does in close attack.
        
        Max 70 characters."""
    
    def far_attack_description(self) -> str:
        """Provides a description of what this critter does in far attack.
        
        Max 70 characters."""

    def move_description(self) -> str:
        """Provides a description of this critter moving.
        
        Max 70 characters."""

    def die(self) -> str:
        """Provides a message upon death of this critter.  Max 70 chars."""
    
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, new_health):
        if new_health < 1:
            raise ValueError("health value must be at least 1.")
        self._health = new_health
    
    @property
    def defense(self):
        return self._defense
    @defense.setter
    def defense(self, new_defense):
        if new_defense < 0:
            raise ValueError("defense value must not be negative.")
        self._defense = new_defense
    
    @property
    def close_attack_power(self):
        return self._close_attack_power
    @close_attack_power.setter
    def close_attack_power(self, new_close_attack_power):
        if new_close_attack_power < 0:
            raise ValueError("close_attack_power value must not be negative.")
        self._close_attack_power = new_close_attack_power

    @property
    def far_attack_power(self):
        return self._far_attack_power
    @far_attack_power.setter
    def far_attack_power(self, new_far_attack_power):
        if new_far_attack_power < 0:
            raise ValueError("far_attack_power value must not be negative.")
        if new_far_attack_power > 6:
            raise ValueError("far_attack_power value must not be bigger than 6")
        self._far_attack_power = new_far_attack_power

    @property
    def far_attack_range(self):
        return self._far_attack_range
    @far_attack_range.setter
    def far_attack_range(self, new_far_attack_range):
        if new_far_attack_range < 0:
            raise ValueError("far_attack_range value must not be negative.")
        if self.far_attack_power > 0 and new_far_attack_range < 2:
            msg = "\nIf far_attack_power > 0, then it must have "
            msg += "far_attack_range > 2."
            raise ValueError(msg)
        if new_far_attack_range > 0 and self.far_attack_power == 0:
            msg = "\nIf far_attack_range > 0, then it must have "
            msg += "far_attack_power > 0."
            raise ValueError(msg)
        self._far_attack_range = new_far_attack_range

    @property
    def speed(self):
        return self._speed
    @speed.setter
    def speed(self, new_speed):
        if new_speed < 1:
            raise ValueError("speed value must be at least 1.")
        self._speed = new_speed
    
    @property
    def location(self):
        return (self.x, self.y)
    @location.setter
    def location(self, new_location):
        self.x = new_location[0]
        self.y = new_location[1]

def distance(x_1: int, y_1: int, x_2: int, y_2: int) -> int:
    """Each square, diagonal, horizontal or vertical, counts as 1."""
    return max(abs(x_2 - x_1), abs(y_2 - y_1))

def direction_to_xy(self, direction: int) -> (int | None, int | None):
    """Convert direction to xy-coordinates"""
    if direction == 1: 
        return 1, 0
    elif direction == 2: 
        return 1, 1
    elif direction == 3:
        return 0, 1
    elif direction == 4:
        return -1, 1
    elif direction == 5:
        return -1, 0
    elif direction == 6:
        return -1, -1
    elif direction == 7:
        return 0, -1
    elif direction == 8:
        return 1, -1
    else:
        return None, None

def xy_to_direction(self, x: int, y: int) -> int | None:
    """Convert xy-coordinates to direction."""
    if x == 1 and y == 0:
        return 1
    elif x == 1 and y == 1:
        return 2
    elif x == 0 and y == 1:
        return 3
    elif x == -1 and y == 1:
        return 4
    elif x == -1 and y == 0:
        return 5
    elif x == -1 and y == -1:
        return 6
    elif x == 0 and y == -1:
        return 7
    elif x == 1 and y == -1:
        return 8
    else:
        return None