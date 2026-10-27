import math


class Tile:



    def __init__(self,value:int = 0 ):
        self.paths = {"top": None,"right": None, "bottom": None, "left": None }
        self.value = value


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
        self.board =  [[Tile(value=size-1-y+x) for y in range(size)] for x in range(size)]

        for x in range(size):
            for y in range(size):
                paths = [
                    self.board[x - 1][y] if x > 0 else None,  # top
                    self.board[x][y + 1] if y < size - 1 else None,  # right
                    self.board[x + 1][y] if x < size - 1 else None,  # bottom
                    self.board[x][y - 1] if y > 0 else None,  # left
                ]
                self.board[x][y].set_all_paths(paths)


    @staticmethod
    def remove_path(side, tile:Tile):
        opposites = {"top": "bottom", "bottom": "top", "right": "left", "left": "right"}
        other_tile = tile.get_path(side=side)
        if other_tile:
            tile.set_path(side=side,target_tile=None)
            other_tile.set_path(side=opposites[side],target_tile=None)
        else:
            raise ValueError("no path found")
