from unittest import TestCase
# Student critter lives in RenJasmine.py. Critter and distance stay in critter.py.
from RenJasmine import DuskLynx
from critter import Critter, distance

# Test class name matches the critter class.
class TestDuskLynx(TestCase):
    """Test my Critter class."""

    def setUp(self):
        self.lynx = DuskLynx()
        self.lynx.location = (5, 5)
        self.lynx.team = 0
        self.lynx.used_attack = False

    def _foe(self, x, y, health=5, defense=4, close=4, far=4, far_range=4, speed=4):
        """Place an enemy Critter. Stats must add up to 25."""
        foe = Critter(health, defense, close, far, far_range, speed)
        foe.location = (x, y)
        foe.team = 1
        return foe

    def _melee(self, x, y, health=8):
        """An enemy with claws only: 8 + 4 + 5 + 0 + 0 + 8 = 25."""
        foe = self._foe(x, y, health=8, defense=4, close=5, far=0, far_range=0, speed=8)
        foe.health = health
        return foe

    def _archer(self, x, y, health=5):
        """An enemy that can shoot: 5 + 5 + 0 + 4 + 5 + 6 = 25."""
        foe = self._foe(x, y, health=5, defense=5, close=0, far=4, far_range=5, speed=6)
        foe.health = health
        return foe

    def test_dunder_str(self):
        """Make sure __str__ returns string of length no more than 70 chars."""
        text = str(self.lynx)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertLessEqual(len(text), 70)
        self.assertIn("Dusk Lynx", text)

    def test_dunder_repr(self):
        """Make sure evaluating __repr__ actually produces an equivalent obj."""
        copy = eval(repr(self.lynx))
        self.assertIsInstance(copy, DuskLynx)
        for stat in (
            "health",
            "defense",
            "close_attack_power",
            "far_attack_power",
            "far_attack_range",
            "speed",
        ):
            self.assertEqual(getattr(self.lynx, stat), getattr(copy, stat))
        self.assertEqual(
            self.lynx.health
            + self.lynx.defense
            + self.lynx.close_attack_power
            + self.lynx.far_attack_power
            + self.lynx.far_attack_range
            + self.lynx.speed,
            Critter.total_points,
        )

    def test_close_attack(self):
        """Try out a few scenarios, check that your code decides correctly."""
        # Enemy one square east. Direction 1.
        foe = self._melee(6, 5)
        self.assertEqual(self.lynx.close_attack(self.lynx, foe), 1)

        # Enemy one square northwest. Direction 6.
        foe.location = (4, 4)
        self.assertEqual(self.lynx.close_attack(self.lynx, foe), 6)

        # Someone two squares away is outside close range.
        far = self._melee(5, 7)
        self.assertEqual(self.lynx.close_attack(self.lynx, far), 0)

        # A list argument is treated the same as separate arguments.
        self.assertEqual(self.lynx.close_attack([self.lynx, self._melee(6, 5)]), 1)

    def test_far_attack(self):
        """Try out a few scenarios, check that your code decides correctly."""
        # Distance 3 is inside far_attack_range (3). Shoot that square.
        foe = self._melee(5, 8)
        self.assertEqual(distance(5, 5, 5, 8), 3)
        self.assertEqual(self.lynx.far_attack(self.lynx, foe), (5, 8))

        # Distance 2 is still a far attack (adjacent is the only exclusion).
        foe.location = (5, 7)
        self.assertEqual(self.lynx.far_attack(self.lynx, foe), (5, 7))

        # Adjacent enemies are not legal far-attack targets.
        foe.location = (6, 5)
        self.assertIsNone(self.lynx.far_attack(self.lynx, foe))

        # Distance 4 is past far_attack_range.
        foe.location = (5, 9)
        self.assertEqual(distance(5, 5, 5, 9), 4)
        self.assertIsNone(self.lynx.far_attack(self.lynx, foe))

    def test_move(self):
        """Try out a few scenarios, check that your code decides correctly."""
        # Adjacent and the attack is still available: claw.
        melee = self._melee(6, 5)
        self.assertEqual(self.lynx.move(self.lynx, melee), 10)

        # In far range, attack still available: shoot. Distance 5 -> 8 is 3.
        melee.location = (5, 8)
        self.assertEqual(self.lynx.move(self.lynx, melee), 11)

        # Melee enemy beyond range: step straight toward them (south, direction 3).
        self.lynx.location = (0, 0)
        melee.location = (0, 9)
        self.assertEqual(self.lynx.move(self.lynx, melee), 3)

        # Already in the shooting band, attack spent, melee enemy: hold at max range.
        self.lynx.location = (5, 5)
        self.lynx.used_attack = True
        melee.location = (5, 8)
        self.assertEqual(self.lynx.move(self.lynx, melee), 0)

        # Too close to a melee enemy after the attack: back straight away (north).
        melee.location = (5, 7)
        self.assertEqual(distance(5, 5, 5, 7), 2)
        self.assertEqual(self.lynx.move(self.lynx, melee), 7)

        # Adjacent melee enemy, attack already used: step west, off their square.
        melee.location = (6, 5)
        self.assertEqual(self.lynx.move(self.lynx, melee), 5)

        # Archer in the distance: close in. Straight south from (0, 0) to (0, 9).
        self.lynx.location = (0, 0)
        self.lynx.used_attack = False
        archer = self._archer(0, 9)
        self.assertEqual(self.lynx.move(self.lynx, archer), 3)

        # Archer already in far range, attack spent: keep closing (south).
        self.lynx.location = (5, 5)
        self.lynx.used_attack = True
        archer.location = (5, 8)
        self.assertEqual(self.lynx.move(self.lynx, archer), 3)

        # Archer adjacent, attack available: still take the close attack.
        self.lynx.used_attack = False
        archer.location = (6, 5)
        self.assertEqual(self.lynx.move(self.lynx, archer), 10)

        # Nobody else on the board: stand still.
        self.assertEqual(self.lynx.move(self.lynx), 0)

        # Backing up would leave the board, and no other step gains distance.
        self.lynx.location = (9, 5)
        self.lynx.used_attack = True
        melee.location = (7, 5)
        self.assertEqual(self.lynx.move(self.lynx, melee), 0)

        # Passing the critters as one list matches passing them separately.
        self.lynx.location = (5, 5)
        self.lynx.used_attack = False
        melee.location = (6, 5)
        self.assertEqual(self.lynx.move([self.lynx, melee]), 10)

    def test_close_attack_description(self):
        """Check close_attack_description.

        It should return a string of length no more than 70 chars."""
        text = self.lynx.close_attack_description()
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertLessEqual(len(text), 70)

    def test_far_attack_description(self):
        """Check far_attack_description.

        It should return a string of length no more than 70 chars."""
        text = self.lynx.far_attack_description()
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertLessEqual(len(text), 70)

    def test_move_description(self):
        """Check move_description.

        It should return a string of length no more than 70 chars."""
        text = self.lynx.move_description()
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertLessEqual(len(text), 70)

    def test_die(self):
        """Make sure die returns string of length no more than 70 chars."""
        text = self.lynx.die()
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertLessEqual(len(text), 70)

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
