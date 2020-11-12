import numpy as np

class Cyclist(object):

    def __init__(self, profile, peloton):
        if profile == 'a':
            file = "cyclist_files/all_rounder.txt"
        elif profile == 's':
            file = "cyclist_files/sprinter.txt"
        elif profile == 'c':
            file = "cyclist_files/climber.txt"

        self.height = np.loadtxt(file)[0]
        self.mass = np.loadtxt(file)[1]
        self.frontal = np.loadtxt(file)[2]
        self.drag = np.loadtxt(file)[3]
        self.w_prime = np.loadtxt(file)[4]
        self.critical_power = np.loadtxt(file)[5]

        if peloton == 'n':
            self.peloton_coefficient = 1.0
        elif peloton == 's':
            self.peloton_coefficient = 0.96
        elif peloton == 'l':
            self.peloton_coefficient = 0.86

    #returns force needed for cyclist to travel at 
    # given speen
    def wind_force(self, air_density, speed):
        f = 0.5 * self.frontal * air_density * self.drag * (speed * speed) * self.peloton_coefficient
        return f

    #returns frictional rolling force
    def roll_force(self, friction, gravity):
        f = friction * self.mass * gravity
        return f

    #returns gravitational rolling force
    def grav_force(self, gravity, slope):
        f = self.mass * gravity * slope
        return f

    #returns total force needed for cyclist to move
    def total_force(self, wind, roll, gravity):
        t = wind + roll + gravity
        return t

    #returns wind coefficient of speed for given 
    # power(v^3)
    def wind_power(self, air_density):
        p = 0.5 * self.frontal * air_density * self.drag * self.peloton_coefficient
        return p

    #returns frictional and gravitational coefficient 
    # of speed for given power (v^1)
    def roll_grav_power(self, roll_f, grav_f):
        p = roll_f + grav_f
        return p

    #function to calculate power from speed
    def power(self, route, speed):

        c = cyclist
        r = route

        wind = self.wind_force(r.air_density, speed)
        grav = self.grav_force(r.gravity, r.slope)
        roll = c.roll_force(r.friction, c.mass, r.gravity)
        total_f = total_force(wind, grav, roll)

        p = total_f * speed

        return p

    #function to calculate speed from power
    def speed(self, route, power, i):

        r = route

        roll = self.roll_force(r.friction, r.gravity)
        grav = self.grav_force(r.slopes[i], r.gravity)
        wind = self.wind_power(r.air_density)
        rg = self.roll_grav_power(roll, grav)

        poly = [-wind, 0, -rg, power]
        speed = np.roots(poly)[2]
        sp = str(speed)[1:15]
        return float(sp)