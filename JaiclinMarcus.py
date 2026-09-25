import critter

class MyMonster(critter.Critter):
    """Your docstring here.  Please re-name this class.
    
    You should also change all the attribute values.  The 6 attribute values
    need to add up to a total of 25."""
    def __init__(self):
        # health must be at least 1.
        self.health = 5
        # defense can't be negative.
        self.defense = 4 
        # close_attack_power can't be negative.  If this is zero, you don't
        #   have to write a close_attack() method.
        self.close_attack_power = 4 
        # if far_attack_power > 0, then far_attack_range has to be between 
        #   2 and 9.  If far_attack_range is between 2 & 9, far_attack_power
        #   has to be > 0.
        # far_attack_power has to be between 0 and 6.
        # far_attack_range has to be 0 or between 2 and 9.
        # If both far_attack_power & _range are 0, you don't have to write a
        #   far_attack() method.
        self.far_attack_power = 4 
        self.far_attack_range = 4 
        # speed must be at least 1.
        self.speed = 4
        # Notice that this class inherits from critter.Critter. super() 
        #   means that I am calling the __init__() method from critter.Critter.
        super().__init__(
            self.health,
            self.defense,
            self.close_attack_power,
            self.far_attack_power,
            self.far_attack_range,
            self.speed,
        )

    def __str__(self) -> str:
        """Provides a human-friendly description of the critter, max 70 chars"""

    def __repr__(self) -> str:
        """Provides a string that, if executed, would create this critter"""

    def close_attack(self, *critters: critter.Critter) -> int:
        """Decide which opponent to attack, if any in range
        
        Input critters includes all active (living) critters in
            the game, including self.
        Returns a direction to attack.  Directions match .move()
        """

    def far_attack(self, *critters: critter.Critter) -> (int, int):
        """Decide which opponent to attack, if any in range
        
        Input critters includes all active (living) critters in
            the game, including self.
        Returns a location on the board to attack.
        """

    def move(self, *critters: critter.Critter) -> int:
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
        """Provides a description of what this critter does in a close attack"""
    
    def far_attack_description(self) -> str:
        """Provides a description of what this critter does in a far attack"""

    def move_description(self) -> str:
        """Provides a description of this critter moving"""

    def die(self) -> str:
        """Provides a message upon death of this critter.  Max 70 chars."""
    