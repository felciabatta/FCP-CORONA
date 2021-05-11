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
    
    parser.add_argument('--duration', metavar='T', type=int, default=200,
                        help='Simulate for T days')
    
    parser.add_argument('--distancing', metavar='P', type=float, default=0.05,
                        help='Proportion of empty grid squares')
    
    parser.add_argument('--recovery', metavar='P', type=float, default=0.1,
                        help='Probability of recovery (per day)')
    
    parser.add_argument('--infection', metavar='P', type=float, default=0.33,
                        help='Probability of infecting a neighbour (per day)')
    
    parser.add_argument('--reinfection', metavar='P', type=float, default=0.005,
                        help='Probability of losing immunity (per day)')
                        # double check how long immunity lasts for default
    
    parser.add_argument('--death', metavar='P', type=float, default=0.002087,
                        help='Probability of dying when infected (per day)')
                        # default is 0.2%, as it is 'per day',
                        # as roughly 10 days of infection, results in ~2% overall
    
    parser.add_argument('--cases', metavar='N', type=int, default=5,
                        help='Average number of intial cases')
    
    parser.add_argument('--vaccinate', metavar='P', type=float, default=0.0001,
                        help='Probability of vaccination (per day)')
    
    parser.add_argument('--quarantine', metavar='P', type=float, default=0.15,
                        help='Probability of quarantine when infected (per day)')
    
    parser.add_argument('--travel', metavar='P', type=float, default=0.1,
                        help='Probability of travelling while infected (per day)')
    
    parser.add_argument('--mode', metavar='m', type=str, default='animate',
                        help='Choose "animate", or "data" mode')
    
    parser.add_argument('--data', metavar='d', type=str, default='total',
                        help='Choose "total", or "individual" data')
    
    parser.add_argument('--file', metavar='N', type=str, default=None,
                        help='Filename to save to instead of showing on screen')
    
    parser.add_argument('--sim', metavar='N', type=int, default=0,
                        help='Run predetermined simulation')
    
    args = parser.parse_args(args)
    
    
    # Predetermined simulations
    # NOTE: Need some decent names for these, 
    #       could put into another file and convert to bash instead of functions?
    if args.sim==1:
        """Standard simulation, with no measures in place,
           demonstrates phenomenon of waves"""
        sp = subPopulationSim(75,75,pVaccination=0)
        
        sp.randomInfection(0.002)
        
        sim = populationSim([sp])
        
        ani = Animation(sim,args.duration)
        ani.show()
        
    elif args.sim==2:
        """Many cities, with small amounts of travelling between cities, 
           leading to multiple waves"""
        sp = subPopulationSim(50,50,pTravel=0.01,city='')
        sp2 = subPopulationSim(20,20,pTravel=0.01,city='')
        sp3 = subPopulationSim(30,30,pTravel=0.01,city='')
        sp4 = subPopulationSim(50,50,pTravel=0.01,city='')
        sp5 = subPopulationSim(50,50,pTravel=0.01,city='')
        sp6 = subPopulationSim(75,75,pTravel=0.01,city='')
        
        sp.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3,sp4,sp5,sp6])
        
        ani = Animation(sim,args.duration)
        ani.show()
        
    elif args.sim==3:
        """Many cities, with large amounts of travelling between cities, 
           leading to multiple waves, but tending towards an equillibrium,
           with near-constant number of cases"""
        sp = subPopulationSim(50,50,pTravel=0.3,city='')
        sp2 = subPopulationSim(20,20,pTravel=0.3,city='')
        sp3 = subPopulationSim(30,30,pTravel=0.3,city='')
        sp4 = subPopulationSim(50,50,pTravel=0.3,city='')
        sp5 = subPopulationSim(50,50,pTravel=0.3,city='')
        sp6 = subPopulationSim(75,75,pTravel=0.3,city='')
        
        sp.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3,sp4,sp5,sp6])
        
        ani = Animation(sim,args.duration)
        ani.show()
        
    elif args.sim==4:
        """High rate of quarantine vs low quarantine"""
        sp = subPopulationSim(75,75,pTravel=0.0,city='High\nQuarantine',pQuarantine=1,pEndQuarantine=0)
        sp2 = subPopulationSim(75,75,pTravel=0.0,city='Medium\nQuarantine',pQuarantine=0.3,pEndQuarantine=0.1)
        sp3 = subPopulationSim(75,75,pTravel=0.0,city='No\nQuarantine',pQuarantine=0)
        
        sp.randomInfection(0.002)
        sp2.randomInfection(0.002)
        sp3.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3], pInfection=0.33)
        
        ani = animateIndividual(sim,args.duration)
        ani.show()
        
    elif args.sim==5:
        """Lots of vaccination vs no vaccination"""
        sp = subPopulationSim(75,75, pVaccination=0.1, city='High Vaccination')
        sp2 = subPopulationSim(75,75, pVaccination=0.033, city='Medium Vaccination')
        sp3 = subPopulationSim(75,75, pVaccination=0, city='No Vaccination')
        
        sp.randomInfection(0.002)
        sp2.randomInfection(0.002)
        sp3.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3], pInfection=0.33)
        
        ani = animateIndividual(sim,args.duration)
        ani.show()
        
    elif args.sim==6:
        """Lots of combined measures vs no measures"""
        sp = subPopulationSim(75,75, pVaccination=0.033, pQuarantine=0.95, 
                              pEndQuarantine=0.05, pTravel=0,pRecovery=0.2,
                              city='Strict Measures')
        
        sp2 = subPopulationSim(75,75, pVaccination=0.01,pQuarantine=0.3, pTravel=0.1,
                               pRecovery=0.1, city='Some Measures')
        
        sp3 = subPopulationSim(75,75, pVaccination=0,pQuarantine=0, pTravel=0.3,
                               pRecovery=0.075, city='No Measures')
        
        sp.emptyLocation(0.3)
        sp2.emptyLocation(0.1)
        
        
        sp.randomInfection(0.002)
        sp2.randomInfection(0.002)
        sp3.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3], pInfection=0.33)
        
        ani = animateIndividual(sim,args.duration)
        ani.show()
    
    elif args.sim==7:
        """Many cities, to show the effects of 
           population density/social distancing"""
        sp = subPopulationSim(50,50,pTravel=0.01,city='No Distancing')
        sp2 = subPopulationSim(50,50,pTravel=0.01,city='Low Distancing')
        sp3 = subPopulationSim(50,50,pTravel=0.01,city='')
        sp4 = subPopulationSim(50,50,pTravel=0.01,city='Medium Distacing')
        sp5 = subPopulationSim(50,50,pTravel=0.01,city='')
        sp6 = subPopulationSim(50,50,pTravel=0.01,city='High Distancing')
        
        sp.emptyLocation(0)
        sp2.emptyLocation(0.15)
        sp3.emptyLocation(0.3)
        sp4.emptyLocation(0.45)
        sp5.emptyLocation(0.6)
        sp6.emptyLocation(0.75)
        
        sp.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3,sp4,sp5,sp6])
        
        ani = animateIndividual(sim,args.duration)
        ani.show()
        
    elif args.sim==8:
        """Many cities, to show the effects of 
           different death probabilities"""
        sp = subPopulationSim(75,75,pTravel=0.0,pDeath=0.002,city='Minimal Death')
        sp2 = subPopulationSim(75,75,pTravel=0.0,pDeath=0.1,city='Medium Death')
        sp3 = subPopulationSim(75,75,pTravel=0.0,pDeath=0.9,city='High Death')
        
        sp.randomInfection(0.002)
        sp2.randomInfection(0.002)
        sp3.randomInfection(0.002)
        
        sim = populationSim([sp,sp2,sp3])
        
        ani = animateIndividual(sim,args.duration)
        ani.show()
        
    elif args.sim==9:
        """No vaccination vs vaccinating after a period of time"""
        sp = subPopulationSim(75,75, pVaccination=0.1, startVaccination=8, 
                              city='Vaccinate after 8 days')
        # sp2 = subPopulationSim(75,75, pVaccination=0.033, city='Medium Vaccination')
        sp3 = subPopulationSim(75,75, pVaccination=0, city='No Vaccination')
        
        sp.randomInfection(0.002)
        # sp2.randomInfection(0.002)
        sp3.randomInfection(0.002)
        
        sim = populationSim([sp,sp3], pInfection=0.33)
        
        ani = animateIndividual(sim,args.duration)
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
        cities[0].randomInfection( args.cases/(args.cities*args.size**2) )
        
        sim = populationSim(cities, args.infection)
        
        
        if args.mode=='animate':
            if args.data=='total':
                ani = Animation(sim, args.duration)
            elif args.data=='individual':
                ani = animateIndividual(sim, args.duration)
            ani.show()
        
        elif args.mode=='data':
            if args.data=='total':
                for day in range(args.duration):
                    sim.update()
                print(sim.collectData())
            elif args.data=='individual':
                for day in range(args.duration):
                    sim.update()
                for sp in sim.subPopulations:
                    print(f'\n{sp.city}\n',sp.collectData())
    


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
    
    
    
    