import math
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    TOP = (-1, 0)
    RIGHT = (0, 1)
    BOTTOM = (1, 0)
    LEFT = (0, -1)

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


    def set_path(self, side,target_tile:"Tile"):
        if side in self.paths.keys():
            self.paths[side] = target_tile
        else:
            raise ValueError("Invalid side")


    def get_path(self, side):
        if side in self.paths:
            return self.paths[side]
        else:
            raise ValueError("Invalid side")

    def set_all_paths(self, paths: list[Tile]):
        if len(paths) == 4:
            keys = ("top", "right", "bottom", "left")
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
    @staticmethod
    def remove_path(side, tile:Tile):
        opposites = {"top": "bottom", "bottom": "top", "right": "left", "left": "right"}
        other_tile = tile.get_path(side=side)
        if other_tile:
            tile.set_path(side=side,target_tile=None)
            other_tile.set_path(side=opposites[side],target_tile=None)
        else:
            raise ValueError("no path found")

    def stuck(self,chosen):
        if chosen ==("",self.current_tile.value):
            self.current_tile.value +=2
            self.previous_tile +=3
            return True
        else:
            return False

    # chooses witch direction to go next
    def choose_tile(self):
        chosen = ("", self.current_tile.value)
        directions=self.current_tile.paths.keys()

        for direction in directions:
            if self.current_tile.paths[direction] is not None:
                if self.current_tile.paths[direction].value<chosen[1]:
                    chosen = (direction,self.current_tile.paths[direction].value)


        self.stuck(chosen)
        print(chosen)
        return chosen[0]

    # goes to the next tile and saves prevous tile as current
    def go_to_next_tile(self,direction):
        self.previous_tile,self.current_tile = self.current_tile,self.current_tile.paths[direction]
        if self.current_tile.value==0:
            self.solved = True
            print(self.current_tile)


if __name__ == "__main__":
    maze = Maze(size=5)
    while not maze.solved:
        direction = maze.choose_tile()
        maze.go_to_next_tile(direction= direction)

