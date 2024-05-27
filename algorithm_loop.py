import math
import sys
import numpy as np

from auxiliar_functions import selection_roulette
from auxiliar_functions import recombination
from auxiliar_functions import mutation
from auxiliar_functions import survival
#--------------------------------------------------------#
# Pop generator
#--------------------------------------------------------#

def initial_uniform_pop(pop_size,classname,map_size,center,*args):
  coordinates = []
  sqrt = math.sqrt
  floor = math.floor

  step = map_size/(sqrt(pop_size)-1)

  for i in range(floor(sqrt(pop_size))):
    for j in range(floor(sqrt(pop_size))):
      x = i * step - abs(map_size)/2 + center[0]
      y = j * step - abs(map_size)/2 + center[1]
      X = np.array([x,y])
      indi = classname(X,*args)
      coordinates.append(indi)

  return coordinates

def random_pop_generator(pop_size,classname,map_size,center,*args):
  pop = []
  sqrt = math.sqrt
  floor = math.floor

  step = map_size/(sqrt(pop_size)-1)

  for i in range(floor(sqrt(pop_size))):
    for j in range(floor(sqrt(pop_size))):
      x = i * step - abs(map_size)/2 + center[0]
      y = j * step - abs(map_size)/2 + center[1]
      X = np.array([x,y])
      indi = classname(X,*args)
      pop.append(indi)

  return pop


#--------------------------------------------------------#
# Genetic Algorithm
#--------------------------------------------------------#

def genetic_algorithm(function_name,recombination_name,mutation_name,sigma,classname,map_size,parent_size=50,population_size=100,center=[0,0],alpha=0.02,max_it=50):
  population = initial_uniform_pop(population_size,classname,map_size,center,alpha)
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

def particle_swarm_optimization(experiment_name,classname,map_size,bounds,population_size=100,center=[0,0],max_it=50,C1=2,C2=2,w=0.6):
  population = initial_uniform_pop(population_size,classname,map_size,center,w,C1,C2)
  generation_data=[]
  gen_number=0

  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)

    print("G = "+str(gen_number))
    # for p in population:
    #   p.print()

    fun = getattr(sys.modules["auxiliar_functions"],experiment_name)
    population = fun(population)

  return generation_data

def diferencial_evolution(experiment_name,classname,map_size,bounds,population_size=100,center=[0,0],R=0.8,Cr=0.7,max_it=50):
  min_b, max_b = np.asarray(bounds).T
  diff = np.fabs(min_b - max_b)
  population = initial_uniform_pop(population_size,classname,map_size,center,R,Cr,min_b,diff)
  generation_data=[]
  gen_number=0

  while gen_number < max_it:
    gen_number=gen_number+1

    generation_data.append(population)

    fun = getattr(sys.modules["auxiliar_functions"],experiment_name)
    population = fun(population)

  return generation_data
