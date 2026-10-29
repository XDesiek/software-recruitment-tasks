from unittest import case

from maze_brain import Direction


class RobotBrain:
    def __init__(self):
        self.driving = False
        self.moves =[]
        self.previous_encoder_values =(0.2,0.2) #(0.2,0.2)
        self.current_rotation=Direction.TOP


    def travel(self,encoders):
        enc_val= ((self.previous_encoder_values[0],encoders[0].getValue()),
                         (self.previous_encoder_values[1],encoders[1].getValue()))
        DRIVEVALUE=5.85#d/r=alpha(5.85)
        TURNVALUE=2.22# pi*R/2r = alpha(1.99) ??not working
        match self.moves[0]:
            # drive FORWARD
            case Direction.TOP:
                if  abs(enc_val[0][1]-enc_val[0][0]) < DRIVEVALUE and \
                    abs(enc_val[1][1]-enc_val[1][0]) < DRIVEVALUE:
                    return (3.0,3.0)
            # turn RIGHT
            case Direction.RIGHT:
                if  abs(enc_val[0][1]-enc_val[0][0]) < TURNVALUE and \
                    abs(enc_val[1][1]-enc_val[1][0]) < TURNVALUE:
                    return (1.5, -1.5)
            # turn LEFT
            case Direction.LEFT:
                if  abs(enc_val[0][1]-enc_val[0][0]) < TURNVALUE and \
                    abs(enc_val[1][1]-enc_val[1][0]) < TURNVALUE:
                    return (-1.5, 1.5)

        self.current_rotation=self.current_rotation.rotate(self.moves[0])
        del self.moves[0]
        self.previous_encoder_values=(enc_val[0][1],enc_val[1][1])
        if not self.moves:
            self.driving = False
        return(0.0,0.0)

    def set_travel(self,direction):
        self.driving = True
        # TODO:kardynalne żeby cos takiego pisac
        for x in range(3):
            direction =direction.rotate(self.current_rotation)


        match direction:
            # drive FORWARD
            case Direction.TOP:
                self.moves.append(Direction.TOP)

            # drive BACKWARD
            case Direction.BOTTOM:
                self.moves.extend([Direction.RIGHT,
                                   Direction.RIGHT,
                                   Direction.TOP
                                   ])

            # drive LEFTWARD
            case Direction.LEFT:
                self.moves.extend([Direction.LEFT,
                                   Direction.TOP
                                   ])

            # drive RIGHTWARD
            case Direction.RIGHT:
                self.moves.extend([Direction.RIGHT,
                                   Direction.TOP
                                   ])


    def scan(self,sensors):
        walls = []

        for direction,sensor in zip(Direction,sensors):
            if sensor>85:
                walls.append(direction.rotate(self.current_rotation))
        return walls