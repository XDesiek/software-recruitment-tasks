from dataclasses import dataclass, field
from enum import Enum



class Direction(Enum):
    TOP = (-1, 0)
    RIGHT = (0, 1)
    BOTTOM = (1, 0)
    LEFT = (0, -1)
    def __repr__(self) -> str:
        return self.name
    def __str__(self) -> str:
        return self.name

    def _rotate_by_steps(self, steps: int) -> "Direction":
        members = list(Direction)
        return members[(members.index(self) + steps) % len(members)]
    @property
    def clockwise(self) -> "Direction":
        return self._rotate_by_steps(1)

    @property
    def counter_clockwise(self) -> "Direction":
        return self._rotate_by_steps(-1)

    @property
    def opposite(self) -> "Direction":
        return self._rotate_by_steps(2)

    # rotates directios from map to robot
    def rotate(self,current_rotation):
        steps = list(Direction).index(current_rotation)
        return self._rotate_by_steps(steps)

    # rotates directios from robot to map
    def anty_rotate(self,current_rotation):
        steps = list(Direction).index(current_rotation)
        return self._rotate_by_steps(-steps)

# ----------------------------------------------------------------------------------------------------------
@dataclass
class Tile:

    value: int = 0
    paths: dict[Direction, "Tile | None"] = field(default_factory=dict,repr=False)


    def set_all_paths(self, paths: list[Tile]):
        self.paths.update(zip(Direction, paths))


# -------------------------------------------------------------------------------------------------------
class Maze:

    def __init__(self,size):
        self.size = size
        self.solved = False
        self.previous_tile = None
        self.board = [[Tile(value=size-1-y+x) for y in range(size)] for x in range(size)]
        self.current_tile = self.board[size-1][0]

        # creating connections between the tiles on the board
        for x in range(size):
            for y in range(size):
                paths = [
                    self.board[x - 1][y] if x > 0 else None,  # top
                    self.board[x][y + 1] if y < size - 1 else None,  # right
                    self.board[x + 1][y] if x < size - 1 else None,  # bottom
                    self.board[x][y - 1] if y > 0 else None,  # left
                ]
                self.board[x][y].set_all_paths(paths)



    # creates wall (deletes paths from and to a tile)
    def set_wall(self,direction):
        other_tile = self.current_tile.paths[direction]
        if other_tile:
            self.current_tile.paths[direction]=None
            other_tile.paths[direction.opposite]=None
        elif other_tile is not None:
            raise ValueError("Invalid direction")


    def set_walls(self,walls):
        for wall in walls:
            self.set_wall(wall)

    # adds to the current path so its less likely to go there again
    def stuck(self,chosen,times_stuck):
        if chosen[0] is None:
            self.current_tile.value +=2
            if not times_stuck:
                self.previous_tile.value +=3
            return True
        else:return False

    # chooses witch direction to go next
    def choose_tile(self):
        times_stuck = 0
        while True:
            valid_options=[
                (direction,tile.value)
                for direction, tile in self.current_tile.paths.items()
                if tile is not None]

            valid_options.append((None, self.current_tile.value))

            chosen = min(
                valid_options,
                key=lambda option: option[1]
            )
            # solving a case where there is not a tile with a lower value
            if self.stuck(chosen,times_stuck):times_stuck+=1
            else:break

        return chosen[0]

    # goes to the next tile and saves prevous tile as current
    def go_to_next_tile(self,direction):
        self.previous_tile,self.current_tile = self.current_tile,self.current_tile.paths[direction]
        if self.current_tile.value==0:
            self.solved = True