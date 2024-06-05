# Questions

All experiments are inside `main.ipynb`, they can be opened either with `jupyter notebook` or google colab

Most of the code other than the experiments are inside the other files. In a nutshell:

- `individual_class.py` has the classes that can be instantiated as particles/individuals
- `auxiliar_functions.py` has some functions that can be used together with Individual class
- `algorithm_loop.py` has the main loop that will be used directly on experiments
- `graphical_visualization.py` some more auxiliar functions to help us visualize stuff, such as fitness curve

Codes implements a table that stores all values of each algorithm
``` python
final_fitness_table = {}
final_fitness_table["mini"] = {}
final_fitness_table["mean"] = {}
```

For example, for question 1:
``` python
option="PSO 1"
final_fitness_table["mini"][option] = []
final_fitness_table["mean"][option] = []
```

To plot the fitness we just need to call `plot_fitness_over_generation(final_fitness_table)`

For the other stuff, ALL of them are shown inside a single cell and are copied for each question.

A quick explanation of every variable used, some of the same arguments are used and described as comments

- `max_it`: maximum number of generations
- `num_tests`: number of tests to be used
- `experiment_name`: this will dynamically call the correct auxiliary function
- `c1_variable`: the c1 variable
- `c2_variable`: the c2 variable
- `w_variable`: the w variable
- `bounds`: I didn't need it, so I didn't implement it

For the population stuff
- `population_size`: defines the population size
- `map_size`: total size of the domain map. This is used to spread the initial generation
- `center`: center of the initial "spread" of the population, use this to create a less clean number as the starting point. In my case, I use inside rosenbrock the algorithm finding $x* = (1,1)$ too quickly.

## Individual 

The abstract **Individual** class inside `individual_class.py` is responsible to store its chromosomes 
(which in this case is also the position), and the fitness value. 

For the sake of simplicity it also stores static options as static, for example, the global minimum 
And variables as object members, for example, the position

Eventually it will evolve using other auxiliary functions, defined inside `auxiliar_functions.py`.

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

For the Differential Evolution Algorithm
- **mut_cross_select_2**: will join the dimensions based on the difference between individuals, then multiply by `R`, then exchange dimensions (genes) with probability `Cr`, then, if position is better, will replace the position
- **mut_cross_select_4**: Same as above but with 4 parents mutation

For the Particle Swarm Optimization:
- **cloud_particle_loop**: will search for the local minimum nearby and the global minimum and perform comparisons. 
Then, it will update the particle velocity and its position. Check the last lines of the `cloud_particle_loop` function

With this, except for the selection algorithm, everything is pretty much done. 
Of course, we still need some auxiliary functions to allow `individuals` to interact with
each other. That will be explained next

## Auxiliar function

As mentioned, those are the functions that will be de facto used by the algorithms individuals.

It includes:

For the Genetic Algorithm:
- **recombination function**: Will gather a list of individual pairs and use them to create a "son" or "sons". Then, will call a specified algorithm `algorithm_name`. All from the algorithms available on the slides
- **selection roullete**: Will gather a weighted list of all fitness and randomly select one from that list. Of course, the bigger the weight, the more likely they are on being selected
- **mutation**: loop through all objects and mutates then one by one. This is used only for the sons
- **survival**: keep the `final_size` individuals with the **best** fitness, kills the rest

For the Differential Evolution Algorithm (base parameters plus two subtractions):
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
- `classname`: Class that will be used as Individual class (by inheriting it, check ipynb)

# Graphical visualization

`graphical_visualization.py`, this is just used to make the graphics.
Notice that most functions have `generation_data`, it will be used to generate the graphics mostly.

Also, notice that most functions have `function_name`,`recombination_name`,`mutation_name` and `sigma`, they are use to generate the titles only.

- **contour_over_population**: Will generate a contour of the chosen function `ff`

- **get_last_best_ind**: Will get the individual with the best fitness and in the entire scenario and return it. Alongside other characteristics that will later be use to group all `num_tests` scenarios. In this case `num_tests` = 30.

- **plot_fintess_over_generation**: Plot scenarios, giving a graphic of fitness x generation. For mean and minimum. Also shows a limited version with less generations to better visualize

- **store_average_fintess**: Will receive every data of all generations and get the mean and minium of each, I use this just to plot every "scenarios" at the end of the report.

- **store_fitness_pymoo**: The same as the function above, but is modified to work with pymoo data

- **store_fitness_pyswarm**: The same as the function above, but is modified to work with pyswarm
