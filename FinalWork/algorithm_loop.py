import math
import sys
import numpy as np

from auxiliar_functions import selection_roulette
from auxiliar_functions import recombination
from auxiliar_functions import mutation
from auxiliar_functions import survival

from auxiliar_functions import deepso_rand_1
from auxiliar_functions import pso_2_bin

from individual_class import IndividualDEEPSO
from individual_class import IndividualPSO
#--------------------------------------------------------#
# Pop generator
#--------------------------------------------------------#

def initial_random_pop(pop_size, bounds, numpy_array=True, dimensions=2, seed=None, center = None):
  if seed is not None:
    np.random.seed(seed)
  points = np.random.uniform(bounds[0],bounds[1],size=(pop_size,dimensions))

  # Move the entire thing to a specific center
  if center is not None:
    points = points + np.array(center)
  return points

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

def particle_swarm_optimization(experiment_name,classname,coordinates,max_it,C1=2,C2=2,w=0.6, bounds=None,vbounds=None):
  population = [classname(coord,w,C1,C2) for coord in coordinates]
  generation_data=[]
  gen_number=0

  match experiment_name:
    case "pso_2_bin":
      fun = pso_2_bin
    case _:
      raise Exception("Unkown experiment name")

  IndividualPSO.gi = None
  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)

    fun = getattr(sys.modules["auxiliar_functions"],experiment_name)
    population = fun(population, bounds, vbounds)
    # IndividualPSO.gi.print()
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

def deepso(experiment_name,classname,coordinates,max_it=100,tcom=0.5,tmut=0.2, bounds=None,vBounds=None,wBounds=None):
  population = [classname(coord,wi0=0.5,wa0=0.5,wc0=0.5,v=np.zeros(len(coord)),p=coord) for coord in coordinates]
  generation_data=[]
  gen_number=0

  match experiment_name:
    case "deepso_rand_1":
      fun = deepso_rand_1
    case _:
      raise Exception("Unkown experiment name")

  IndividualDEEPSO.gi = None
  while gen_number < max_it:
    if gen_number > 60:
      print("NEW GEN NUMBER "+str(gen_number))
    gen_number=gen_number+1
    generation_data.append(population)
    population = fun(population, tmut, tcom, bounds, vBounds, wBounds)
  return generation_data

def deepso_hill_climbing(experiment_name,classname,coordinates,max_it=100,tcom=0.5,tmut=0.2,hc_bound=[-1,1],hc_max_it=10,hc_stops=[10]):
  population = [classname(coord,wi0=0.5,wa0=0.5,wc0=0.5,v=np.zeros(len(coord)),p=coord) for coord in coordinates]
  generation_data=[]
  gen_number=0

  match experiment_name:
    case "deepso_rand_1":
      fun = deepso_rand_1
    case _:
      raise Exception("Unkown experiment name")

  IndividualDEEPSO.gi = None
  while gen_number < max_it:
    gen_number=gen_number+1
    generation_data.append(population)
    population = fun(population, tmut, tcom)

    if gen_number in hc_stops:
      initial_fitness = IndividualDEEPSO.gi.getFitness()
      IndividualDEEPSO.gi = hill_climbing(classname,len(population),IndividualDEEPSO.gi,hc_max_it,hc_bound)
      print("Difference = "+str(IndividualDEEPSO.gi.getFitness() - initial_fitness))
  return generation_data

def hill_climbing(classname,pop_size,cand,max_it,bound,dimensions=2):
  gen_number=0

  while gen_number < max_it:
    gen_number=gen_number+1
    coords = initial_random_pop(pop_size, bound,dimensions=dimensions, center=cand._X)
    generated_population = [classname(coord) for coord in coords]
    generated_population.append(cand)
    cand = min(generated_population,key=lambda x: x.getFitness())
  return cand

def cdeepso(experiment_name,classname,coordinates,max_it=100,tcom=0.5,tmut=0.2, bounds=None,vBounds=None,wBounds=None):
  population = [classname(coord,wi0=0.5,wa0=0.5,wc0=0.5,v=np.zeros(len(coord)),p=coord) for coord in coordinates]
  generation_data=[]
  gen_number=0

  match experiment_name:
    case "deepso_rand_1":
      fun = deepso_rand_1
    case _:
      raise Exception("Unkown experiment name")

  IndividualCDEEPSO.gi = None
  while gen_number < max_it:
    gen_number=gen_number+1
    generation_data.append(population)
    population = fun(population, tmut, tcom, bounds, vBounds, wBounds)
  return generation_data


