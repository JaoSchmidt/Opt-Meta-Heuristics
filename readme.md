## Individual 

The abstract **Individual** class inside `individual_class.py` is responsible to store its cromossomes 
(which in this case is also the position), and the fitness value. 

For the sake of simplicity it also stores static options as static, for example, the global minimum 
And variables as object members, for example, the position

Eventually it will evolve using other auxiliar functions, defined inside `auxiliar_functions.py`.

- **_fitness_function**: not defined here, will be defined only on its child, e.g. Rosenbrock, Eggholder
- **getFitness**: get the current fitness stored inside the object
- **__setFitness**: recalcuate the fitness stored in the object
- **setPosition**: change the individual position and recalculate its value
- **print**: print stuff inside, very usefull for debugging
- **get_data**: get the position and value of the object, useful for generating graphics, tables and etc

----

For the Genetic Algorithm:
- **mutation_creep**: slighty add a change to the current position using a normal distribution and a sigma (that I will define later)
- **mutation_gaussian**: same as creep, but uses the current position as average
- **recombination_`name of recombination`**: Implements a specific crossover algorithm with the invididual itself and some other object. Creates one or more "sons" and return them.

For the Diferential Evolution Algorithm
- **mut_cross_select_2**: will join the dimensions based on the difference between individuals, then multiply by `R`, then exchange dimenisons (genes) with probabilithy `Cr`, then, if position is better, will replace the position
- **mut_cross_select_4**: Same as above but with 4 parents mutation

For the Particle Swarm Optimization:
- **cloud_particle_loop**: will search for the local minimum nearby and the global minimum and perform comparasions. 
Then, it will update the particle velocity and its position. Check the last lines of the `cloud_particle_loop` function

With this, except for the selection algorithm, everything is pretty much done. Of course, we still need some auxiliar functions to allow `individuals` to interact with each other. That will be explained next

## Auxiliar function

As mentioned, those are the functions that will be de facto used by the algorithms individuals.

It includes:

For the Genetic Algorithm:
- **recombination function**: Will gather a list of individual pairs and use them to create a "son" or "sons". Then, will call a specificied algorithm `algorithm_name`. All from the algorithms available on the slides
- **selection roullete**: Will gather a weighted list of all fitness and randomly select one from that list. Of course, the bigger the weight, the more likely they are on being selected
- **mutation**: loop through all objects and mutates then one by one. This is used only for the sons
- **survival**: keep the `final_size` individuals with the **best** fitness, kills the rest

For the Diferential Evolution Algorithm (base parameters plus two subtractions):
- **de_rand**: random value for all parameters
- **de_best**: random value for all parameters, except base parameter which is the best
- **de_current_to_best**: random value for all parameters, except the second parameter

For the Particle Swarm Optimization:
- **pso_2_bin**: this function will just loop through all particles, executing cloud_particle_loop on them
Check `individual_class.py`

# Algorithm Main Loop (For the PSO)

Inside `algorithm_loop.py`, check `initial_pop_generator`. It is now separated from the main loop,
it will create a bunch of initial coordinates uniformly

**initial_pop_generator**: Will create `pop_size` individuals uniformly spread inside the problem's domain.
- `map_size`: total size of the domain map. This is used to spread the initial generation
- `center`: center of the initial "spread" of the population, use this to create a less clean number as the starting point. In my case, I use inside rosenbrock the algorithm finding $x* = (1,1)$ too quickly.
- `population_size`: size of population
- `dimensions`: default to 2, number of dimensions of the problem, will reflect on the returning coordinates
- `numpy_array`: check true if needed to return a numpy array

**PSO**: This the actual loop of the entire algorithm, it will make the following:
- `max_it`: maximum number of generations
- `gen_number` count the number of generations processed by the algorithm. The only purpose is to limit the number of generations of the loop.
- `generation_data` has the purpose of storing data to be used later, with tables, graphics, etc
- `classname`: Class that will be used as Individual class (inheriting)

# Graphical visualization

This is just used to make the graphics
Notice that most functions have `generation_data`, it will be used to generate the graphics mostly.

Also, notice that most functions have `function_name`,`recombination_name`,`mutation_name` and `sigma`, they are use to generate the titles only.

- **contour_over_population**: Will generate a contour of the choosen function `ff`, see the [Eggholder example](#scrollTo=y3ANjaNExTd1&line=4&uniqifier=1) to see the difference between both functions. The only reason I have both is because it works for now, I will probably replace everything with numpy next time. As mentioned in the presentation, the "more" red, the newer the generations.

- **get_last_best_ind**: Will get the individual with the best fitness and in the entire scenario and return it. Alongside other characterirstics that will later be use to group all `num_tests` scenarios. In this case `num_tests` = 30.

- **plot_fintess_over_generation**: Plot scenarios, giving a graphic of fitness x generation. For mean and minimum. Also shows a limited version with less generations to better visualize

- **store_average_fintess**: Will receieve every data of all generations and get the mean and minium of each, I use this just to plot every "scenarios" at the end of the report.

- **store_fitness_pymoo**: The same as the function above, but is modified to work with pymoo data

- **store_fitness_pymoo**: The same as the function above, but is modified to work with pyswarm

# Questions

All code below was implemented by hand. Using the code right above `REPORT`

All code implements roulette as recombination algorithm . For the other options, ALL of them are shown inside each "option" and will once again be shown in the final table.

Exempli gratia: `option1`, `option2`, `option3`, `pymoo`, etc

I didn't how many of each to put so I made 8 manual implementations on a whim, and 1 pymoo implementation because I didn't have time to build more.

A quick explanation, of every variable used, some of the same arguments are used and described [here](#scrollTo=S6AQpw9AI53r&line=19&uniqifier=1):

- `final_table`: dictionary used to store average and minimum values of each scenario

- `final_fitness_table`: dictionary used to store average and minimum values of each scenario

- `max_it`: maximum number of generation
- `num_tests`: number of tests to be used
- `experiment_name`: In this case is DE/Rand/1
- `r_variable`: variable r used during "mutation" process of the DE
- `cr_variable`: variable cr used for the crossover of genes
- `title`: used on the final table and plot to differentiate the algorithms
- `population_size`: defines the population at the end of the loop
- `parent_size`: defines the size of the population that will be select for "reproducing"
- `map_size`: total size of the domain map. This is used to spread the initial generation
- `center`: center of the initial "spread" of the population, use this to create a less clean number as the starting point. In my case, I use inside rosenbrock the algorithm finding $x* = (1,1)$ too quickly.
- `num_tests`: number of tests to be made before creating the final statistic. Central Limit theorem. The choice here is to make 30.
