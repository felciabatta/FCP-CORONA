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
    
    parser.add_argument('--cities', metavar='N', type=int, default=2,
                        help='Create N cities')
    
    parser.add_argument('--duration', metavar='T', type=int, default=100,
                        help='Simulate for T days')
    
    parser.add_argument('--distancing', metavar='P', type=float, default=0.05,
                        help='Proportion of empty grid squares')
    
    parser.add_argument('--recovery', metavar='P', type=float, default=0.1,
                        help='Probability of recovery (per day)')
    
    parser.add_argument('--infection', metavar='P', type=float, default=0.3,
                        help='Probability of infecting a neighbour (per day)')
    
    parser.add_argument('--reinfection', metavar='P', type=float, default=0.001,
                        help='Probability of losing immunity (per day)')
                        # double check how long immunity lasts for default
    
    parser.add_argument('--death', metavar='P', type=float, default=0.002087,
                        help='Probability of dying when infected (per day)')
                        # default should probably be much lower that 2%, as it is per day,
                        # maybe 0.2% as roughly 10 days period of infection
    
    parser.add_argument('--cases', metavar='P', type=float, default=0.001,
                        help='Probabilty of initial infection')
    
    parser.add_argument('--vaccinate', metavar='P', type=float, default=0.0001,
                        help='Probability of vaccination (per day)')
    
    parser.add_argument('--quarantine', metavar='P', type=float, default=0.15,
                        help='Probability of quarantine when infected (per day)')
    
    parser.add_argument('--travel', metavar='P', type=float, default=0.03,
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
        # sp.emptyLocation(0.3)
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
        
    elif args.sim==8:
        """High rate of quarantine vs low quarantine"""
        sp = subPopulationSim(100,100,pTravel=0.0,pQuarantine=1,pEndQuarantine=0)
        sp2 = subPopulationSim(100,100,pTravel=0.0,pQuarantine=0)
        
        sp.emptyLocation(0.1)
        sp2.emptyLocation(0.05)
        
        sp.randomInfection(0.005)
        sp2.randomInfection(0.005)
        
        sim = populationSim([sp,sp2], pInfection=0.25)
        
        ani = Animation(sim,100)
        ani.show()
        
    elif args.sim==9:
        """Lots of vaccination vs no vaccination"""
        sp = subPopulationSim(100,100, pVaccination=0.01)
        sp2 = subPopulationSim(100,100, pVaccination=0.001)
        
        sp.randomVaccination(0.2)
        sp2.randomVaccination(0.01)
        
        sp.emptyLocation(0.05)
        sp2.emptyLocation(0.05)
        
        sp.randomInfection(0.005)
        sp2.randomInfection(0.005)
        
        sim = populationSim([sp,sp2], pInfection=0.25)
        
        ani = Animation(sim,100)
        ani.show()
        
    elif args.sim==10:
        """Lots of combined measures vs no measures"""
        sp = subPopulationSim(100,100, pVaccination=0.01, pQuarantine=0.95, 
                              pEndQuarantine=0, pTravel=0,pRecovery=0.2)
        sp2 = subPopulationSim(100,100, pVaccination=0.001,pQuarantine=0, pTravel=0.5,
                               pRecovery=0.075)
        
        sp.randomVaccination(0.05)
        
        sp.emptyLocation(0.05)
        
        sp.randomInfection(0.005)
        sp2.randomInfection(0.005)
        
        sim = populationSim([sp,sp2], pInfection=0.25)
        
        ani = Animation(sim,100)
        ani.show()
        
    else:
        # custom simulation input, via bash
        cities = []
        for i in range(args.cities):
            cities.append(subPopulationSim(width=args.size, height=args.size, pDeath=args.death,
                              pInfection=args.infection, pRecovery=args.recovery, 
                              pReinfection=args.reinfection, pTravel=args.travel,
                              pQuarantine=args.quarantine, city=f"City {i+1}",
                              pEndQuarantine=0.05, pVaccination = args.vaccinate
                              )
                          )
            
        for sp in cities:
            sp.emptyLocation(args.distancing)
        cities[0].randomInfection(args.cases)
        
        
        sim = populationSim(cities, args.infection)
        
        ani = Animation(sim, args.duration)
        ani.show()
    
        



if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
    
    
    
    