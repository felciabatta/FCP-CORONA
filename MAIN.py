#!/usr/bin/env python3

import argparse
from SIMULATION.py import subPopulationSim

def main(*args):

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
    parser.add_argument('--cases', metavar='N', type=int, default=2,
                        help='Number of initial infected people')
    parser.add_argument('--plot', action='store_true',
                        help='Generate plots instead of an animation')
    parser.add_argument('--file', metavar='N', type=str, default=None,
                        help='Filename to save to instead of showing on screen')
    args = parser.parse_args(args)
    
    simulation = subPopulationSim(args.size, args.size,
                            args.recovery, args.infection, args.death)
    
if __name__ == "__main__":
    
    # CLI entry point. The main() function can also be imported and called
    # with string arguments.
    
    import sys
    main(*sys.argv[1:])