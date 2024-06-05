import math
import sys
import numpy as np

from auxiliar_functions import selection_roulette
from auxiliar_functions import recombination
from auxiliar_functions import mutation
from auxiliar_functions import survival

from  individual_class import IndividualDEEPSO
#--------------------------------------------------------#
# Pop generator
#--------------------------------------------------------#

def initial_uniform_pop(pop_size, map_size, center, numpy_array=True, dimensions=2):
    coordinates = []
    sqrt = math.sqrt
    floor = math.floor

    # Determine the number of points per dimension
    points_per_dimension = floor(sqrt(pop_size ** (1 / dimensions)))
    step = map_size / (points_per_dimension - 1) if points_per_dimension > 1 else map_size

    # Create a recursive function to generate the grid points
    def generate_points(dim, current_point):
        if dim == dimensions:
            if numpy_array:
                coordinates.append(np.array(current_point))
            else:
                coordinates.append(list(current_point))
            return

        for i in range(points_per_dimension):
            point_coordinate = i * step - abs(map_size) / 2 + center[dim]
            generate_points(dim + 1, current_point + [point_coordinate])

    # Start generating points from the first dimension
    generate_points(0, [])
    return coordinates

#--------------------------------------------------------#
# Genetic Algorithm
#--------------------------------------------------------#

def genetic_algorithm(function_name,recombination_name,mutation_name,sigma,classname,map_size,parent_size=50,population_size=100,center=[0,0],alpha=0.02,max_it=50):
  coordinates = initial_uniform_pop(population_size,map_size,center)
  population = [classname(coord,alpha) for coord in coordinates]
  generation_data=[]
  gen_number=0

  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)
    # selection (roullete, fitness)
    parents = selection_roulette(population,parent_size)

    # cross/recombination (arithmetic avarage, geometric avarege, blx_alpha, blx-2-sons, arithmetic, heuristic)
    sons = recombination(parents, recombination_name)

    # mutation (gaussian, creep)
    mutation(sons,sigma,mutation_name)

    # survival
    population = population + sons
    population = survival(population,population_size)

  return generation_data

def particle_swarm_optimization(experiment_name,classname,coordinates,max_it,C1=2,C2=2,w=0.6):
  population = [classname(coord,w,C1,C2) for coord in coordinates]
  generation_data=[]
  gen_number=0

  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)

    fun = getattr(sys.modules["auxiliar_functions"],experiment_name)
    population = fun(population)

  return generation_data

def diferencial_evolution(experiment_name,classname,map_size,bounds,population_size=100,center=[0,0],R=0.8,Cr=0.7,max_it=50):
  min_b, max_b = np.asarray(bounds).T
  diff = np.fabs(min_b - max_b)
  coordinates = initial_uniform_pop(population_size,map_size,center)
  population = [classname(coord,R,Cr,min_b,diff) for coord in coordinates]
  generation_data=[]
  gen_number=0

  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)

    fun = getattr(sys.modules["auxiliar_functions"],experiment_name)
    population = fun(population)

  return generation_data

def deepso(experiment_name,classname,map_size,bounds,population_size=100,center=[0,0],max_it=100,tcom=0.5,tmut=0.5):
  min_b, max_b = np.asarray(bounds).T
  diff = np.fabs(min_b - max_b)
  coordinates = initial_uniform_pop(population_size,map_size,center)
  population = [classname(coord,1,1,1,np.zeros(len(coord)),coord) for coord in coordinates]
  generation_data=[]
  gen_number=0

  IndividualDEEPSO.tcom = tcom
  IndividualDEEPSO.tmut = tmut

  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)

    fun = getattr(sys.modules["auxiliar_functions"],experiment_name)
    population = fun(population)

  return generation_data
