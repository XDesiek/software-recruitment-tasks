from maze_brain import Direction


class RobotBrain:
    def __init__(self):
        self.driving = False
        self.moves =[]
        self.previous_encoder_values =(0.2,0.2) #(0.2,0.2)
        self.current_rotation=Direction.TOP


    def calibrate(self,walls):
            # wall[0] -> kierunek sciany
            # wall[0] -> "dystans" do sciany
            return [wall[0].opposite for wall in walls if wall[1]]


    def travel(self,encoders,back_sensor):
        # DONT CHANGE THE PARAMETERS ON THEIR OWN
        DRIVEVALUE=5.85#d/r=alpha(5.85)
        TURNVALUE=2.22# pi*R/2r = alpha(1.99) ??not working
        DRIVESPEED = 5.0
        TURNSPEED = 1.7#has to be exactly 1.7 if more or less it works has to calibrate more often
        CALIBRATIONSPEED=0.8

        # encoder values
        enc_val= ((self.previous_encoder_values[0],encoders[0].getValue()),
                         (self.previous_encoder_values[1],encoders[1].getValue()))


        match self.moves[0]:
            # calibrate forward
            case (Direction.TOP,"calibrate"):
                if back_sensor>150:
                    return(CALIBRATIONSPEED,CALIBRATIONSPEED)
            # drive FORWARD
            case (Direction.TOP,"drive"):
                if  abs(enc_val[0][1]-enc_val[0][0]) < DRIVEVALUE and \
                    abs(enc_val[1][1]-enc_val[1][0]) < DRIVEVALUE:
                    return (DRIVESPEED,DRIVESPEED)
            # turn RIGHT
            case (Direction.RIGHT,_):
                if  abs(enc_val[0][1]-enc_val[0][0]) < TURNVALUE  and \
                    abs(enc_val[1][1]-enc_val[1][0]) < TURNVALUE:
                    return (TURNSPEED, -TURNSPEED)
            # turn LEFT
            case (Direction.LEFT,_):
                if  abs(enc_val[0][1]-enc_val[0][0]) < TURNVALUE and \
                    abs(enc_val[1][1]-enc_val[1][0]) < TURNVALUE:
                    return (-TURNSPEED, TURNSPEED)


        self.current_rotation=self.current_rotation.rotate(self.moves[0][0])
        self.previous_encoder_values=(enc_val[0][1],enc_val[1][1])
        del self.moves[0]
        if not self.moves:self.driving = False
        return(0.0,0.0)


    def generate_steps(self,direction):
        new_moves =[]

        match direction.anty_rotate(self.current_rotation):
            # drive FORWARD
            case Direction.TOP:
                new_moves.append(Direction.TOP)
            # drive RIGHTWARD
            case Direction.RIGHT:
                new_moves.extend([Direction.RIGHT,Direction.TOP])
            # drive BACKWARD
            case Direction.BOTTOM:
                new_moves.extend([Direction.RIGHT,Direction.RIGHT,Direction.TOP])
            # drive LEFTWARD
            case Direction.LEFT:
                new_moves.extend([Direction.LEFT,Direction.TOP])
        return new_moves


    def set_travel(self,direction,move_type):
        self.driving = True
        new_moves = self.generate_steps(direction)
        self.moves = list(zip(new_moves,[move_type]*len(new_moves)))



    def scan(self,sensors):
        walls = []

        for direction,sensor in zip(Direction,sensors):
            if sensor>85:
                walls.append((
                    direction.rotate(self.current_rotation),sensor
                    if sensor>200
                    else 0 ))
        # returns where the walls are and their "distance" to the wall
        return walls