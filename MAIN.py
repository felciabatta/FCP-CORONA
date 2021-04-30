#!/usr/bin/env python3

import argparse
from SIMULATION import *
from ANIMATION import *

def main(*args):

    """
    Example
    =======
    simulation = subPopulationSim(args.size, args.size,
                            args.recovery, args.infection, args.death)
    """    

    parser = argparse.ArgumentParser(description='Animate an epidemic')
    
    parser.add_argument('--size', metavar='N', type=int, default=50,
                        help='Use a N x N simulation grid')
    
    parser.add_argument('--duration', metavar='T', type=int, default=100,
                        help='Simulate for T days')
    
    parser.add_argument('--recovery', metavar='P', type=float, default=0.1,
                        help='Probability of recovery (per day)')
    
    parser.add_argument('--infection', metavar='P', type=float, default=0.1,
                        help='Probability of infecting a neighbour (per day)')
    
    parser.add_argument('--death', metavar='P', type=float, default=0.005,
                        help='Probability of dying when infected (per day)')
    
    parser.add_argument('--cases', metavar='P', type=float, default=0.05,
                        help='Probabilty of initial infection')
    
    parser.add_argument('--vaccinate', metavar='P', type=float, default=0.01,
                        help='Probability of vaccination (per day)')
    
    parser.add_argument('--quarantine', metavar='P', type=float, default=0.1,
                        help='Probability of quarantine when infected (per day)')
    
    parser.add_argument('--travel', metavar='P', type=float, default=0.1,
                        help='Probability of travelling while infected (per day)')
    
    parser.add_argument('--plot', action='store_true',
                        help='Generate plots instead of an animation')
    
    parser.add_argument('--file', metavar='N', type=str, default=None,
                        help='Filename to save to instead of showing on screen')
    
    parser.add_argument('--sim', metavar='N', type=int, default=0,
                        help='Run predetermined simulation')
    
    args = parser.parse_args(args)
    
    
    # Predetermined simulations
    # NOTE: Need some decent names for these, 
    #       could put into another file and convert to bash instead of functions?
    if args.sim==1:
        simTestDays(10)
    if args.sim==2:
        simTestPop(10)
    if args.sim==3:
        simTest3(10)
    elif args.sim==4:
        simTest4(10)
    else:
        print("Nothing to do yet")
    
    sim = subPopulationSim(100,100)
    sim.randomInfection(0.05)
    ani = Animation(sim,100)
    ani.show()
        



if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
    
    
    
    