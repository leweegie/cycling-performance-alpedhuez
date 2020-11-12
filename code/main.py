from Cyclist import Cyclist
from route import Route
import math
import numpy as np
import matplotlib.pyplot as plt

def power_vs_times(cyclist, route, powers, savefile):
        
    c = cyclist
    r = route

    times = []

    for i in range(len(powers)):
        total_time = 0
        for j in range (len(r.slopes)):
            sp = c.speed(r, powers[i], j)
            distance = float(r.distances[j])
            total_time += distance / sp

        minutes = total_time/60
        times.append(minutes)

    np.savetxt(savefile, np.column_stack([powers, times]))

def unsteady_legtimes(cyclist, route, input, file1, file2):

    c = cyclist
    r = route
    w_primes = []
    times = []
    powers = []
    w_primes.append(c.w_prime)
    powers.append(input[0])
    times.append(0)

    for i in range(len(r.slopes)):
        power = float(input[i])
        #print(power)
        sp = c.speed(r, power, i)
        distance = float(r.distances[i])
        t = distance / sp
        if power > c.critical_power:
            possible_t = c.w_prime / (power - c.critical_power)
            if t > possible_t:
                d_possible = sp * possible_t
                d_remain = r.distances[i] - d_possible
                CP_sp = c.speed(r, c.critical_power, i)
                t_remain = d_remain / CP_sp
                leg_time = t_remain + possible_t
                c.w_prime = 0.0
                powers.append(c.critical_power)
            elif t == possible_t:
                leg_time = t
                c.w_prime = 0.0
                powers.append(c.critical_power)
            else:
                leg_time = t
                c.w_prime = c.w_prime - (t * (power - c.critical_power))
                powers.append(power)
            w_primes.append(c.w_prime)
        else:
            w_primes.append(c.w_prime)
            leg_time = t
            powers.append(power)
        if i ==0:
            times.append(leg_time)
        else:
            times.append(leg_time + times[i])

    np.savetxt(file1, np.column_stack([times, w_primes]))
    np.savetxt(file2, np.column_stack([times, powers]))

def plot_function(filename, graphname, title, x, y):

    X = np.loadtxt(filename)[:,0]
    Y = np.loadtxt(filename)[:,1]

    plt.plot(X, Y, linewidth = 0.5)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.title(title)
    plt.savefig(graphname)
    plt.show()

def plot_function_Y1Y2_vs_X(y1_filename, y2_filename, 
                            graphname, title, x, y, 
                            y1, y2):

    Y1 = np.loadtxt(y1_filename)[:,1]
    Y2 = np.loadtxt(y2_filename)[:,1]
    X = np.loadtxt(y1_filename)[:,0]

    plt.plot(X, Y1, linewidth = 0.5, label = y1)
    plt.plot(X, Y2, linewidth = 0.5, label = y2)
    plt.legend()
    plt.ylabel(y)
    plt.xlabel(x)
    plt.title(title)
    plt.savefig(graphname)
    plt.show()

def plot_function_Y1Y2_vs_X_different_scales(y1_filename, 
                                            y2_filename, 
                                            graphname, 
                                            title, 
                                            x, 
                                            y1, 
                                            y2):

    Y1 = np.loadtxt(y1_filename)[:,1]
    Y2 = np.loadtxt(y2_filename)[:,1]
    X = np.loadtxt(y1_filename)[:,0]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel(x)
    ax1.set_ylabel(y1, color=color)
    ax1.set(ylim = (0, 80000))
    ax1.plot(X, Y1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that 
                       #shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(y2, color=color)
    ax2.set(ylim = (0, 700))
    ax2.plot(X, Y2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title(title)
    plt.savefig(graphname)
    plt.show()
        
def plot_function_w_errors(filename, graphname, 
    title, x, y):

    X = np.loadtxt(filename)[:,0]
    Y = np.loadtxt(filename)[:,1]
    errors = np.loadtxt(filename)[:,2]

    plt.plot(X, Y, linewidth = 0.5)
    plt.errorbar(X, Y, linewidth = 0.5, yerr = errors, 
        ecolor = 'red')
    plt.ylabel(y)
    plt.xlabel(x)
    plt.title(title)
    plt.savefig(graphname)
    plt.show()

def main():
    #route constants
    route_file  = "route_files/alpe.txt"
    gravity     = 9.807    # earth
    air_density = 1.226    # sea level
    friction    = 0.005    # asphalt road

    #cyclist constants
    p               = 'n' # n = isolated rider, 
                          # s = small four man, 
                          # l = large 121 man
    c_s             = 15  # speed of cyclist
    power           = np.linspace(200, 450, 41)

    solo1 = Cyclist('s', 'n')
    solo2 = Cyclist('c', 'n')

    four_peloton = Cyclist('c', 's')
    large_peloton = Cyclist('a', 'l')
    r = Route(gravity, air_density, friction, route_file)

    legs = len(r.slopes)
    push = 540
    cp = 350
    solo_powers = [cp, cp, cp, cp, 
        cp, cp, cp, cp, 
        cp, cp, cp, cp, 
        push, push]

    powers = []
    
    for i in range (len(r.slopes)):
        powers.append(solo2.critical_power + 7)
    
    #unsteady_legtimes(solo1, r, solo_powers, 
    #    'wPrime_vs_time/alpe/solo_unsteady_sprint.dat', 
    #    'power_vs_time_wPrime/alpe/solo_unsteady_sprint.dat')
    #unsteady_legtimes(solo2, r, powers, 
    #    'wPrime_vs_time/alpe/solo_steady.dat',
    #    'power_vs_time_wPrime/alpe/solo_steady.dat')
    #unsteady_legtimes(large_peloton, r, powers, 
    #   'wPrime_vs_time/alpe/large_peloton.dat', 
    #   'power_vs_time_wPrime/alpe/large_peloton.dat')

    #plot_function_Y1Y2_vs_X_different_scales('wPrime_vs_time/alpe/solo_unsteady_sprint.dat', 
    #                                            'power_vs_time_wPrime/alpe/solo_unsteady_sprint.dat', 'wPrime_vs_time/alpe/sprint.png', 
    #                                                'W prime & power vs Time (Sprinter)', 'Time (s)', 'W Prime (J)', 'Power (W)')

    '''
    power_vs_times(peloton, r, power, 
        'power_vs_time/largePeloton.dat')
    '''
    plot_function_Y1Y2_vs_X('steady_solo_legtimes.dat', 
        'unsteady_solo_legtimes.dat', 
        'steady_vs_unsteady_legs_climber.png', 
        'Legtimes for Steady vs. Unsteady Power Models', 'Leg #', 'Time(s)', 
        'Steady Power', 'Unsteady Power')
    

main()
