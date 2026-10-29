import math
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    TOP = (-1, 0)
    RIGHT = (0, 1)
    BOTTOM = (1, 0)
    LEFT = (0, -1)
    def __repr__(self) -> str:
        return self.name

    @property
    def clockwise(self) -> "Direction":
        members = list(Direction)
        return members[(members.index(self) + 1) % len(members)]

    @property
    def counter_clockwise(self) -> "Direction":
        members = list(Direction)
        return members[(members.index(self) - 1) % len(members)]

    @property
    def opposite(self) -> "Direction":
        members = list(Direction)
        return members[(members.index(self) + 2) % len(members)]

    def rotate(self,current_rotation):
        match current_rotation:
            case Direction.TOP:
                return  self
            case Direction.RIGHT:
                return self.clockwise
            case Direction.BOTTOM:
                return self.opposite
            case Direction.LEFT:
                return self.counter_clockwise


# ----------------------------------------------------------------------------------------------------------
@dataclass
class Tile:

    value: int = 0
    paths: dict[Direction, "Tile | None"] = field(default_factory=dict,repr=False)


    def set_all_paths(self, paths: list[Tile]):
        if len(paths) == 4:
            keys = (Direction.TOP, Direction.RIGHT, Direction.BOTTOM, Direction.LEFT)
            self.paths.update(zip(keys, paths))
        else:
            raise ValueError("Invalid number of paths")

# -------------------------------------------------------------------------------------------------------
class Maze:

    def __init__(self,size):
        self.size = size
        self.board =  [[Tile(value=size-1-y+x) for y in range(size)] for x in range(size)]
        self.current_tile = self.board[size-1][0]
        self.previous_tile = None
        self.solved = False


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
    def stuck(self,chosen):
        if chosen[0] is None:
            self.current_tile.value +=2
            self.previous_tile.value +=3
            return True
        else:return False

    # chooses witch direction to go next
    def choose_tile(self):
        while True:
            valid_options=(
                (direction,tile.value)
                for direction, tile in self.current_tile.paths.items()
                if tile is not None)

            chosen = min(
                valid_options,
                key=lambda option: option[1]
            )
            if chosen[1] >self.current_tile.value: chosen = (None, self.current_tile.value)
            if not self.stuck(chosen):
                break

        return chosen[0]

    # goes to the next tile and saves prevous tile as current
    def go_to_next_tile(self,direction):
        self.previous_tile,self.current_tile = self.current_tile,self.current_tile.paths[direction]
        if self.current_tile.value==0:
            self.solved = True





