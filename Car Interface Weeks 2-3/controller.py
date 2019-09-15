import random

class Car_Interface():

    '''
    Intialize car interface object.  Model is default to simple.
    If simple acceleration will roughly be a linear combination
    of the corresponding factors.  model = "complex" introduces
    some nonlinearities
    '''
    def __init__(self, model = "simple"):

        if (model != "simple" and model != "complex"):
            raise Exception(f"Illegal argument model can only be 'simple' or 'complex' not {model}")

        self.model = model

        #Variables to keep track of the car's current state
        self.position = 0
        self.velocity = 0
        self.accel = 0

        self.steering_angle = 0

        self.gear = None

        #Constants corresponding to the car pedals
        self.ACCELERATOR = 0
        self.BRAKE = 1

        #Constants corrsponding to car gears
        self.FORWARD = 0
        self.REVERSE = 1

        #Coefficients corresponding to the motion dynamics
        self.rolling_bias = 0.01
        self.friction_constant = 0.11

        self.accelerator_weight = 0.1
        self.brake_weight = -0.25

        #Initialize of state log
        self.log = {"time": [], "position": [], "velocity": [], "acceleration": []}
        self.max_log_length = 50000
        self.log_drop_if_max = 5000

        #Variables to keep track of time (seconds)
        self.T = 0
        #Corresponds to simulations internal discrete time step
        self.dt = 0.05
        self.num_readings = 0
    
    #Depress the same pedal by the same amount for a specified time
    def apply_control_for_time(self, pedal, amount, time):
        
        if (time <= 0):
            raise Exception(f"Time must be positive, not {time}")
        
        for _ in range(int(time / self.dt)):
            self.apply_control(pedal, amount)
        

    #Depress the specified pedal by the specified amount for one dt time step
    def apply_control(self, pedal, amount):

        if (self.gear is None):
            raise Exception("Please set gear before applying control")

        if (pedal not in [None, self.ACCELERATOR, self.BRAKE]):
            raise Exception(f"Invalid pedal provided, {pedal}")

        if (amount < 0 or amount > 1):
            raise Exception(f"Amount must be between 0 and 1, not {amount}")

        if (self.gear is None):
            return

        if (pedal is None):
            self.accel = 0

        elif (pedal == self.ACCELERATOR):
            
            if (self.model == "simple"):
                self.accel = self.accelerator_weight * amount

            elif (self.model == "complex"):
                self.accel = self.accelerator_weight * amount * (0.5 + 0.5 * self.velocity)

        elif (pedal == self.BRAKE):

            if (self.model == "simple"):
                self.accel = self.brake_weight * amount

            elif (self.model == "complex"):
                self.accel = self.brake_weight * amount * (self.velocity + 0.1)

        self.accel += self.rolling_bias

        if (self.gear == self.REVERSE):
            self.accel *= -1

        self.accel -= self.friction_constant * self.velocity

        self.gear_force()

        self.log_data()

        self.position += self.velocity * self.dt + 0.5 * self.accel * (self.dt ** 2)
        self.velocity += self.accel * self.dt


        self.T += self.dt
        

    #Ensures that car can only move in direction of gear
    def gear_force(self):

        if (self.gear == self.FORWARD):
            self.velocity = max(self.velocity, 0)
            if (self.velocity == 0):
                self.accel = max(self.accel, 0)
        elif(self.gear == self.REVERSE):
            self.velocity = min(self.velocity, 0)
            if (self.velocity == 0):
                self.accel = min(self.accel, 0)

    #Used for switching gear (None, the initial state inhibits movement)
    def set_gear(self, gear):
        if (gear != self.FORWARD and gear != self.REVERSE):
            raise Exception(f"Invalid gear provided {gear}")

        if (gear != self.gear):
            if (self.gear is None):
                self.gear = gear
            else:
                if (abs(self.velocity) < 0.01):
                    self.gear = gear
                else:
                    raise Exception(f"Speed must be below 0.01, current speed: {abs(self.velocity)}")


    #Logs data regarding the current state, dumping previous logs if exceeding memory
    def log_data(self):

        self.log["position"].append(self.add_noise(self.position, noise_mag = 0.01))
        self.log["velocity"].append(self.add_noise(self.velocity, noise_mag = 0.002))
        self.log["acceleration"].append(self.add_noise(self.accel, noise_mag = 0.002))
        self.log["time"].append(self.T)
        if (len(self.log["time"]) > self.max_log_length):
            self.log["position"] = self.log["position"][self.log_drop_if_max:]
            self.log["velocity"] = self.log["velocity"][self.log_drop_if_max:]
            self.log["acceleration"] = self.log["acceleration"][self.log_drop_if_max:]
            self.log["time"] = self.log["time"][self.log_drop_if_max:]
        self.num_readings += 1

    #Since position is a relative measure you are free to zero at will
    def zero_position(self):
        self.position = 0

    #Adds noise used for log readings
    def add_noise(self, x, noise_mag):
        return x - noise_mag + (2 * noise_mag) * random.random()

    #Steer to desired angle (-1 (right) to 1 (left))
    def steer_to(self, ang):
        self.steering_angle = max(-1, min(ang, 1))

