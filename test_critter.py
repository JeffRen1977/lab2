from unittest import TestCase
# You'll need to change this next line to import from your file.
from critter import *

# Change the name in the next line to match your class name.
class TestCritter(TestCase):
    """Test my Critter class."""
    def test_dunder_str(self):
        """Make sure __str__ returns string of length no more than 70 chars."""
    
    def test_dunder_repr(self):
        """Make sure evaluating __repr__ actually produces an equivalent obj."""

    def test_close_attack(self):
        """Try out a few scenarios, check that your code decides correctly."""

    def test_far_attack(self):
        """Try out a few scenarios, check that your code decides correctly."""

    def test_move(self):
        """Try out a few scenarios, check that your code decides correctly."""

    def test_close_attack_description(self):
        """Check close_attack_description. 
        
        It should return a string of length no more than 70 chars."""

    def test_far_attack_description(self):
        """Check far_attack_description. 
        
        It should return a string of length no more than 70 chars."""

    def test_move_description(self):
        """Check move_description. 
        
        It should return a string of length no more than 70 chars."""

    def test_die(self):
        """Make sure die returns string of length no more than 70 chars."""

    def test_init(self):
        """Test input validations.  See __init__ docstring for details."""
        msg = "Critter with too many points does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            too_many_pts = Critter(
                Critter.total_points // 6 + Critter.total_points % 6 + 1, 
                Critter.total_points // 6, 
                Critter.total_points // 6, 
                Critter.total_points // 6, 
                Critter.total_points // 6, 
                Critter.total_points // 6,
            )
        msg = "Critter with not enough points does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            not_enough_pts = Critter(
                Critter.total_points // 6 + Critter.total_points % 6 - 1, 
                Critter.total_points // 6, 
                Critter.total_points // 6, 
                Critter.total_points // 6, 
                Critter.total_points // 6, 
                Critter.total_points // 6,
            )
        msg = "Critter with negative health does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_health = Critter(
                -1, 
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5,
            )
        msg = "Critter with zero health does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_health = Critter(
                0, 
                Critter.total_points // 5 + Critter.total_points % 5 , 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5,
            )
        msg = "Critter with negative defense does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_defense = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                -1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5,
            )
        msg = "Critter with negative close_attack_power "
        msg += "does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_close_attack_power = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                Critter.total_points // 5, 
                -1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5,
            )
        msg = "Critter with negative far_attack_power "
        msg += "does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_far_attack_power = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                -1, 
                Critter.total_points // 5, 
                Critter.total_points // 5,
            )
        msg = "Critter with far_attack_power too large "
        msg += "does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_far_attack_power = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                7, 
                Critter.total_points // 5, 
                Critter.total_points // 5,
            )
        msg = "Critter with negative far_attack_range "
        msg += "does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_far_attack_range = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                -1, 
                Critter.total_points // 5,
            )
        msg = "Critter with far_attack_power > 0 needs to have "
        msg += "far_attack_range of at least 2."
        with self.assertRaises(ValueError, msg = msg):
            bad_far_attack_mix = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 - 1, 
                Critter.total_points // 5,
                Critter.total_points // 5,
                Critter.total_points // 5,
                1,
                Critter.total_points // 5,
            )
        msg = "Critter with far_attack_range > 0 needs to have "
        msg += "far_attack_power > 0."
        with self.assertRaises(ValueError, msg = msg):
            bad_far_attack_mix = Critter(
                Critter.total_points // 5 + Critter.total_points % 5, 
                Critter.total_points // 5,
                Critter.total_points // 5,
                0,
                Critter.total_points // 5,
                Critter.total_points // 5,
            )
        msg = "Critter with negative speed does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_speed = Critter(
                Critter.total_points // 5 + Critter.total_points % 5 + 1, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                -1,
            )
        msg = "Critter with zero speed does not raise ValueError."
        with self.assertRaises(ValueError, msg = msg):
            neg_speed = Critter(
                Critter.total_points // 5, 
                Critter.total_points // 5 + Critter.total_points % 5 , 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                Critter.total_points // 5, 
                0,
            )

    def test_distance(self):
        """Check distance in all four directions."""
        critter_1 = Critter(5, 4, 4, 4, 4, 4)
        critter_2 = Critter(5, 4, 4, 4, 4, 4)
        critter_1.location = (5, 5)
        # above and left
        critter_2.location = (2, 1)
        self.assertEqual(distance(critter_1.x, critter_1.y, 
            critter_2.x, critter_2.y), 4)
        # above and right
        critter_2.location = (9, 0)
        self.assertEqual(distance(critter_1.x, critter_1.y, 
            critter_2.x, critter_2.y), 5)
        # below and left
        critter_2.location = (3, 8)
        self.assertEqual(distance(critter_1.x, critter_1.y, 
            critter_2.x, critter_2.y), 3)
        # below and right
        critter_2.location = (10, 8)
        self.assertEqual(distance(critter_1.x, critter_1.y, 
            critter_2.x, critter_2.y), 5)
