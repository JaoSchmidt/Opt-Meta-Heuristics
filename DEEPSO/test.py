from graphical_visualization import get_last_best_ind
from graphical_visualization import store_average_fitness
from graphical_visualization import contour_over_population
from graphical_visualization import plot_fitness_over_generation

from algorithm_loop import deepso
from algorithm_loop import initial_uniform_pop

from individual_class import IndividualDEEPSO

class Rosenbrock(IndividualDEEPSO):
  def _fitness_function(self,X,a=1,b=100):
    x,y = X
    return pow((a - x),2) + b * pow((y - x**2),2)

def ff(X,a=1,b=100):
  x,y = X
  return (a - x)**2 + b*(y - x**2)**2

final_fitness_table = {}
final_fitness_table["mini"] = {}
final_fitness_table["mean"] = {}

tmut_variable = 1
tcom_variable = 1
experiment_name="deepso_rand_1"
option="DEEPSO 1"

# initial and final pop stuff
population_size = 10000
map_size = 10 # size of a square of the map
# slighty move center to avoid getting into the minimum too quickly
center = [0.3120312,0.2212314]
num_tests = 10 # number of tests to make
max_it = 100

final_fitness_table["mini"][option] = []
final_fitness_table["mean"][option] = []

lazy_title = [option,experiment_name,"tcom = "+str(tcom_variable),"tmut = "+str(tmut_variable)]
for _ in range(0,num_tests):
  coordinates = initial_uniform_pop(population_size,map_size,center,dimensions=2)
  generation_data = deepso(experiment_name,
                                Rosenbrock,
                                coordinates,
                                max_it=max_it,
                                tcom=0.94,
                                tmut=0.05)
  store_average_fitness(generation_data,final_fitness_table,option,num_tests)

contour_over_population(generation_data,', '.join(lazy_title),ff,map_size)
min(generation_data[max_it-1],key=lambda x: x.getFitness()).print()
plot_fitness_over_generation(final_fitness_table)
