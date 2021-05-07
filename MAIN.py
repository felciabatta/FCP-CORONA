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
        
    elif args.sim==2:
        simTestPop(10)
        
    elif args.sim==3:
        simTest3(10)
        
    elif args.sim==4:
        simTest4(10)
        
    elif args.sim==5:
        sp = subPopulationSim(100,100)
        sp.emptyLocation(0.3)
        sp.randomInfection(0.001)
        
        sim = populationSim([sp])
        
        ani = Animation(sim,200)
        ani.show()
        
    elif args.sim==6:
        sp = subPopulationSim(50,50,pTravel=0.03)
        sp2 = subPopulationSim(50,50,pTravel=0.03)
        
        sp.emptyLocation(0.3)
        sp2.emptyLocation(0.2)
        
        sp.randomInfection(0.001)
        
        sim = populationSim([sp,sp2])
        
        ani = Animation(sim,100)
        ani.show()
        
    elif args.sim==7:
        sp = subPopulationSim(50,50,pTravel=0.023)
        sp2 = subPopulationSim(50,30,pTravel=0.021)
        sp3 = subPopulationSim(50,60,pTravel=0.021)
        sp4 = subPopulationSim(20,30,pTravel=0.021)
        sp5 = subPopulationSim(20,20,pTravel=0.021)
        sp6 = subPopulationSim(20,20,pTravel=0.021)
        
        sp.emptyLocation(0.3)
        sp.randomInfection(0.001)
        
        sim = populationSim([sp,sp2,sp3,sp4,sp5,sp6])
        
        ani = Animation(sim,100)
        ani.show()
        
    else:
        print("Nothing to do yet")
    
        



if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
    
    
    
    