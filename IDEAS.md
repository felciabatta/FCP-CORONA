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

An idea to add a class for each person, inorder to track how many days each person has been infected or in quarintine
or anything of the such

Within this class we could have differnet death probabilities given age of a person i.e. have a certain percentage of
the population over an age and they have a higher death probability, or a catergory of people with underlying conditions


VACCINATION:
- rather than having teh vaccine from the start we introduce it after a couple days
- can decide on when to introduce the vaccine by how severe the virus is, the more deadly the quciker it is made
- if we have different death probabilities for different age catergories it can start by vaccinating the people who are
most likely to die
