"""Jasmine Ren's critter for Lab 2: DuskLynx.

DuskLynx is a one-on-one skirmisher. It shoots an opponent that has no far
attack while standing at the edge of its own range, and it walks in on an
opponent that can shoot back. An adjacent opponent is clawed once per round.
"""

import critter

# Board coordinates run from 0 through 9.
BOARD_MIN = 0
BOARD_MAX = 9


class DuskLynx(critter.Critter):
    """A twilight lynx that keeps its distance, then claws if cornered.

    Point budget (these six values must add up to 25):
        health 5, defense 2, close attack 3,
        far attack 6, far range 3, speed 6.
    """

    def __init__(self):
        # health must be at least 1.
        self.health = 5
        # defense can't be negative.
        self.defense = 2
        # close_attack_power can't be negative.
        self.close_attack_power = 3
        # far_attack_power is between 0 and 6.
        # far_attack_range is 0, or between 2 and 9 when power is positive.
        self.far_attack_power = 6
        self.far_attack_range = 3
        # speed must be at least 1.
        self.speed = 6
        super().__init__(
            self.health,
            self.defense,
            self.close_attack_power,
            self.far_attack_power,
            self.far_attack_range,
            self.speed,
        )

    def __str__(self) -> str:
        """Provides a human-friendly description of the critter, max 70 chars."""
        return "Dusk Lynx, a twilight hunter with claws and a piercing cry."

    def __repr__(self) -> str:
        """Provides a string that, if executed, would create this critter."""
        return "DuskLynx()"

    def close_attack(self, *critters: critter.Critter) -> int:
        """Claw the opponent when they are on a neighboring square.

        This lab is one-on-one, so the list is self plus one opponent.
        Directions match move(). Returns 0 when the opponent is not adjacent.
        """
        if self.x is None or self.y is None:
            return 0
        foe = self._opponent(critters)
        if foe is None or self._dist(foe) != 1:
            return 0
        return critter.xy_to_direction(foe.x - self.x, foe.y - self.y)

    def far_attack(self, *critters: critter.Critter) -> tuple:
        """Shoot the opponent when they are inside far range, but not adjacent.

        Returns the opponent's (x, y), or None when they are out of range.
        """
        if self.x is None or self.y is None:
            return None
        foe = self._opponent(critters)
        if foe is None:
            return None
        dist = self._dist(foe)
        if 2 <= dist <= self.far_attack_range:
            return (foe.x, foe.y)
        return None

    def move(self, *critters: critter.Critter) -> int:
        """Choose one action against the single opponent.

        0    stand still
        1-8  step (see the direction diagram on Critter.move)
        10   close attack, when the opponent is adjacent
        11   far attack, when 2 <= distance <= far_attack_range

        One attack is allowed per round (self.used_attack). After that, a
        melee-only opponent is kept at the edge of far range. An opponent
        that can shoot is approached, because trading shots at their range
        is worse.
        """
        if self.x is None or self.y is None:
            return 0
        target = self._opponent(critters)
        if target is None:
            return 0

        dist = self._dist(target)

        if not self.used_attack and self.close_attack_power > 0 and dist == 1:
            return 10
        if (
            not self.used_attack
            and self.far_attack_power > 0
            and 2 <= dist <= self.far_attack_range
        ):
            return 11

        if self._should_kite(target):
            if dist < self.far_attack_range:
                step = self._best_step(target, retreat=True)
                if step != 0:
                    return step
            if dist > self.far_attack_range:
                return self._best_step(target, retreat=False)
            return 0

        if dist > 1:
            return self._best_step(target, retreat=False)
        return 0

    def close_attack_description(self) -> str:
        """Provides a description of what this critter does in a close attack."""
        return "The dusk lynx rakes the nearest foe with its claws."

    def far_attack_description(self) -> str:
        """Provides a description of what this critter does in a far attack."""
        return "The dusk lynx hurls a piercing cry across the field."

    def move_description(self) -> str:
        """Provides a description of this critter moving."""
        return "The dusk lynx pads silently from stone to stone."

    def die(self) -> str:
        """Provides a message upon death of this critter. Max 70 chars."""
        return "The dusk lynx fades into twilight and is still."

    def _unpack(self, critters) -> list:
        """Accept either move(self, foe) or move([self, foe])."""
        if len(critters) == 1 and isinstance(critters[0], (list, tuple)):
            return list(critters[0])
        return list(critters)

    def _opponent(self, critters):
        """The other fighter in a one-on-one match. The list includes self."""
        for other in self._unpack(critters):
            if other is self:
                continue
            if other.x is None or other.y is None:
                continue
            return other
        return None

    def _dist(self, other) -> int:
        return critter.distance(self.x, self.y, other.x, other.y)

    def _should_kite(self, enemy) -> bool:
        """Hold far range only when this lynx can shoot and the enemy cannot."""
        return self.far_attack_power > 0 and enemy.far_attack_power <= 0

    def _on_board(self, x: int, y: int) -> bool:
        return BOARD_MIN <= x <= BOARD_MAX and BOARD_MIN <= y <= BOARD_MAX

    def _best_step(self, enemy, retreat: bool) -> int:
        """Pick a legal step that improves distance. 0 means no such step.

        Ties prefer the step aimed most directly at (or away from) the
        opponent, then a straight step over a diagonal, then the lowest
        direction number. The opponent's square is not a legal step.
        """
        aim_x = enemy.x - self.x
        aim_y = enemy.y - self.y
        if retreat:
            aim_x = -aim_x
            aim_y = -aim_y
        old_dist = self._dist(enemy)
        best_rank = None
        best_direction = 0
        for direction in range(1, 9):
            dx, dy = critter.direction_to_xy(direction)
            next_x = self.x + dx
            next_y = self.y + dy
            if not self._on_board(next_x, next_y):
                continue
            if next_x == enemy.x and next_y == enemy.y:
                continue
            new_dist = critter.distance(next_x, next_y, enemy.x, enemy.y)
            if retreat and new_dist <= old_dist:
                continue
            if not retreat and new_dist >= old_dist:
                continue
            progress = new_dist if retreat else -new_dist
            aimed = dx * aim_x + dy * aim_y
            straight = -(abs(dx) + abs(dy))
            rank = (progress, aimed, straight, -direction)
            if best_rank is None or rank > best_rank:
                best_rank = rank
                best_direction = direction
        return best_direction
