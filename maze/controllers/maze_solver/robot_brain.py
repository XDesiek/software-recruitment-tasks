from unittest import case

from maze_brain import Direction


class RobotBrain:
    def __init__(self):
        self.driving = False
        self.moves =[]
        self.previous_encoder_values = (0.0,0.0)
    def travel(self,encoders):
        # print(abs(self.previous_encoder_values[0]-encoders[0].getValue()),abs(self.previous_encoder_values[1]-encoders[1].getValue()))
        encoder_values= ((self.previous_encoder_values[0],encoders[0].getValue()),
                         (self.previous_encoder_values[1],encoders[1].getValue()))
        DRIVEVALUE=5.88
        TURNVALUE=2.22
        # TURNVALUE=1.99
        match self.moves[0]:
            case Direction.TOP:
                if abs(encoder_values[0][1]-encoder_values[0][0]) < DRIVEVALUE and \
                        abs(encoder_values[1][1]-encoder_values[1][0]) < DRIVEVALUE:
                    return (3.0,3.0)
            case Direction.RIGHT:
                if abs(encoder_values[0][1]-encoder_values[0][0]) < TURNVALUE and \
                        abs(encoder_values[1][1]-encoder_values[1][0]) < TURNVALUE:
                    return (1.5, -1.5)
            case Direction.LEFT:
                if abs(encoder_values[0][1]-encoder_values[0][0]) < TURNVALUE and \
                        abs(encoder_values[1][1]-encoder_values[1][0]) < TURNVALUE:
                    return (-1.5, 1.5)
        del self.moves[0]
        self.previous_encoder_values=(encoders[0].getValue(),encoders[1].getValue())
        if not self.moves:
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
                                   Direction.TOP,
                                   Direction.RIGHT
                                  ])
            case Direction.RIGHT:
                self.moves.extend([
                                   Direction.RIGHT,
                                   Direction.TOP,
                                   Direction.LEFT
                                  ])
    def scan(self,sensors):
        walls = []
        for direction in zip(sensors,Direction):
            # print(direction)
            if direction[0]>85:
                walls.append(direction[1])
        return walls