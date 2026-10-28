from unittest import case

from maze_brain import Direction


class RobotBrain:
    def __init__(self):
        self.driving = False
        self.moves =[]
        self.previous_encoder_values = (0.0,0.0)
    def travel(self,encoders):
        if abs(encoders[0].getValue()-self.previous_encoder_values[0]) < 6.28 and abs(encoders[1].getValue()-self.previous_encoder_values[0]) < 6.28:
            match self.moves[0]:
                case Direction.TOP:
                        return (3.0,3.0)
                case Direction.RIGHT:
                        return (3.14, -3.14)
                case Direction.LEFT:
                        return (-3.14, 3.14)
        else:
            del self.moves[0]
            self.previous_encoder_values=( encoders[0].getValue(),encoders[1].getValue())
            self.driving = False
            return(0.0,0.0)

    def set_travel(self,direction):
        self.driving = True
        match direction:
            case Direction.TOP:
                self.moves.append(Direction.TOP)
            case Direction.BOTTOM:
                self.moves.extend([
                                   Direction.RIGHT,
                                   Direction.RIGHT,
                                   Direction.TOP,
                                   Direction.RIGHT,
                                   Direction.RIGHT
                                   ])
            case Direction.LEFT:
                self.moves.extend([
                                   Direction.LEFT,
                                   Direction.BOTTOM,
                                   Direction.RIGHT
                                  ])
            case Direction.RIGHT:
                self.moves.extend([
                                   Direction.RIGHT,
                                   Direction.BOTTOM,
                                   Direction.LEFT
                                  ])
    def scan(self):
        pass