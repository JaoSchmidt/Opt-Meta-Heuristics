# Install
``` bash
pip install numpy pandas
```
## Running
``` bash
jupyter notebook
```


# Short resume

Again, all experiments inside `main.ipynb`, most other files are self-explanatory, as they were for the PSO.

`main.ipynb`, can be opened either with `jupyter notebook` or google colab

All other files:

- `individual_class.py` has the classes that can be instantiated as particles/individuals, `deepso` included
- `auxiliar_functions.py` has some functions that can be used together with Individual class
- `algorithm_loop.py` has the main loop that will be used directly on experiments, hill_climbing included
- `graphical_visualization.py` some more auxiliar functions to help us visualize stuff, such as fitness curve

The code implements a table that stores all values of each experiment (different auxiliar function, different atributes, etc)
``` python
final_fitness_table = {}
final_fitness_table["mini"] = {}
final_fitness_table["mean"] = {}
```

To plot the fitness we just need to call `plot_fitness_over_generation(final_fitness_table)`

For the other important stuff, ALL of them are shown inside a single cell and are the same for each experiment:

- `max_it`: maximum number of generations
- `num_tests`: number of same experiments to be run
- `experiment_name`: this will dynamically call the correct auxiliary function
- `tmut_variable`: the tmut variable
- `tcom_variable`: the tcom variable

- `bounds`: bounds restricting the position and velocity
- `title`: title of the experiment
- `population_size`: defines the population size

I've now switched and use random coordinates, (instead of uniform coordinates), because its easier

### Hill Climbing

The stuff for the hill climbing is inside `algorithm_loop.py`. What I did was take the best individual (gi),
generate some coords around, then select the new best. 

However, this has produced very little improvement for the gi for this specific function.

You can see that because, for the hill climb version, I printed the difference in fitness. 

And it is getting around 10^-5 closer to the global min. Perhaps a different, little more complex algorithm will work. 
Like Newton


## Individual 

The abstract **Individual** class inside `individual_class.py` is responsible to store chromosomes
(which in this case is also the position), and the fitness value. 

For the sake of simplicity it also stores static options as static, for example, the global minimum 
And variables as object members, for example, the position.

Some important functions:

- **_fitness_function**: not defined here, will be defined only on its child, e.g. Rosenbrock, Eggholder, Himmelblau
- **getFitness**: get the current fitness stored inside the object
- **setPosition**: change the individual position and recalculate its fitness
- **print**: print stuff inside, very useful for debugging
- **get_data**: get the position and value of the object, useful for generating graphics, tables and etc

----

For the Genetic Algorithm:
- **mutation_creep**: slightly add a change to the current position using a normal distribution and a sigma (that I will define later)
- **mutation_gaussian**: same as creep, but uses the current position as average
- **recombination_`name of recombination`**: Implements a specific crossover algorithm with the individual itself and some other object. Creates one or more "sons" and return them.

For the Differential Evolution Algorithm
- **mut_cross_select_2**: will join the dimensions based on the difference between individuals, then multiply by `R`, then exchange dimensions (genes) with probability `Cr`, then, if position is better, will replace the position
- **mut_cross_select_4**: Same as above but with 4 parents mutation

For the Particle Swarm Optimization:
- **cloud_particle_loop**: will search for the local minimum nearby and the global minimum and perform comparisons. 
Then, it will update the particle velocity and its position. Check the last lines of the `cloud_particle_loop` function

For the DEEPSO Algorithm:
- **rand_1**: defined inside the deepso sublcass, will execute type rand_1. It is the "pure" deepso as shown in the slides

With this, except for the selection algorithm, everything is pretty much done. 
Of course, we still need some auxiliary functions to allow `individuals` to interact with
each other. That will be explained next

## Auxiliar function

The population will need auxiliary functions, defined inside `auxiliar_functions.py`.

As mentioned, those are the functions that will be de facto used by the algorithms individuals.

It includes:

For the Genetic Algorithm:
- **recombination function**: Will gather a list of individual pairs and use them to create a "son" or "sons". Then, will call a specified algorithm `algorithm_name`. All from the algorithms available on the slides
- **selection roulette**: Will gather a weighted list of all fitness and randomly select one from that list. Of course, the bigger the weight, the more likely they are on being selected
- **mutation**: loop through all objects and mutates then one by one. This is used only for the sons
- **survival**: keep the `final_size` individuals with the **best** fitness, kills the rest

For the Differential Evolution Algorithm (base parameters plus two subtractions):
- **de_rand**: random value for all parameters
- **de_best**: random value for all parameters, except base parameter which is the best
- **de_current_to_best**: random value for all parameters, except the second parameter

For the Particle Swarm Optimization:
- **pso_2_bin**: this function will just loop through all particles, executing cloud_particle_loop on them

For the DEEPSO Algorithm:
- **deepso_rand_1**: This function will just loop through all particles, no memory, no recombination.

# Graphical visualization

`graphical_visualization.py`, this is just used to make the graphics.
Notice that most functions have `generation_data`, it will be used to generate the graphics mostly.

Also, notice that most functions have `function_name`,`recombination_name`,`mutation_name` and `sigma`, they are used to generate the titles only.

- **contour_over_population**: Will generate a contour of the chosen function `ff`

- **get_last_best_ind**: Will get the individual with the best fitness and in the entire scenario and return it. Alongside other characteristics that will later be use to group all `num_tests` scenarios. In this case `num_tests` = 30.

- **plot_fintess_over_generation**: Plot scenarios, giving a graphic of fitness x generation. For mean and minimum. Also shows a limited version with less generations to better visualize

- **store_average_fintess**: Will receive every data of all generations and get the mean and minium of each, I use this just to plot every "scenarios" at the end of the report.

- **store_fitness_pymoo**: The same as the function above, but is modified to work with pymoo data

- **store_fitness_pyswarm**: The same as the function above, but is modified to work with pyswarm
