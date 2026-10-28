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
    def opposite(self) -> "Direction":
        opposites = {
            Direction.TOP: Direction.BOTTOM,
            Direction.BOTTOM: Direction.TOP,
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
        }
        return opposites[self]

@dataclass
class Tile:

    value: int = 0
    paths: dict[Direction, "Tile | None"] = field(default_factory=dict,repr=False)


    def set_path(self, direction,target_tile:"Tile"):
        if direction in self.paths.keys():
            self.paths[direction] = target_tile
        else:
            raise ValueError("Invalid direction")


    def get_path(self, direction):
        if direction in self.paths:
            return self.paths[direction]
        else:
            raise ValueError("Invalid direction")

    def set_all_paths(self, paths: list[Tile]):
        if len(paths) == 4:
            keys = (Direction.TOP, Direction.RIGHT, Direction.BOTTOM, Direction.LEFT)
            self.paths.update(zip(keys, paths))
        else:
            raise ValueError("Invalid number of paths")


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
    def remove_path(self,direction):
        other_tile = self.current_tile.get_path(direction=direction)
        if other_tile:
            self.current_tile.set_path(direction=direction,target_tile=None)
            other_tile.set_path(direction=direction.opposite,target_tile=None)
        elif other_tile is not None:
            raise ValueError("no path found")

    def set_walls(self,walls):
        for wall in walls:
            self.remove_path(direction=wall)


    def stuck(self,chosen):
        if chosen ==(None,self.current_tile.value):
            self.current_tile.value +=2
            self.previous_tile.value +=3
            return True
        else:
            return False

    # chooses witch direction to go next
    def choose_tile(self):
        while True:
            chosen = (None, self.current_tile.value)
            directions=[
                direction
                for direction, tile in self.current_tile.paths.items()
                if tile is not None]

            for direction in directions:
                if self.current_tile.paths[direction].value<chosen[1]:
                    chosen = (direction,self.current_tile.paths[direction].value)
            # TODO:
            if not self.stuck(chosen):
                break

        return chosen[0]

    # goes to the next tile and saves prevous tile as current
    def go_to_next_tile(self,direction):
        self.previous_tile,self.current_tile = self.current_tile,self.current_tile.paths[direction]
        if self.current_tile.value==0:
            self.solved = True





