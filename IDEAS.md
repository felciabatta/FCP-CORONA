Ideas
- Basic grid-like SIR
- SIR + moving people
- SIR + multiple interacting ‘cities’
- SIR + vaccination, immunity limit, isolation

Classes & Methods - In different files
- ‘Community’ - a group of people (eg city)
    - List state of each grid point (SIR,V,Q)
    - Empty grid points
    - Size of grid
    - Rate/probability of infection
    - Total SIR stats
    - Randomise initial conditions
    - ‘Update’ iterates simulation
            - Checks neighbours
- Plot/animation of behaviour 
- Plot/animation of SIR numbers

Functions
- ‘Run sim’

Arguments
- Number of people/grid size
- Number of infected people
- Number of vaccinated people



For everyday a person is infected, increase the chance of them getting a test. 
(corona symptoms dont show up immediatly, but take time to take effect)
also have a flat probability for someone to randomly get tested.

There should also be probablities for a potential false positive or false negative for the test results.
If a person gets a positive result (wether false or not) they will go into quarintine)