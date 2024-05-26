import random
import bisect
from individualclass import Individual
# ----------------------------------------------- #
# GA
# ----------------------------------------------- #

def recombination(individual_list,algorithm_name):
  sons = []
  for par in range(0,len(individual_list),2):
    p1 = individual_list[par]
    p2 = individual_list[par + 1]
    recombination_method = getattr(p1, "recombination_" + algorithm_name)
    sons.append(recombination_method(p2))
  return sons

def selection_roulette(individual_list: list[Individual],final_size):
  # get fitness array
  fit_arr = [x.getFitness() for x in individual_list]
  # get it normalized
  fit_arr = [(x - max(fit_arr)) / (min(fit_arr) - max(fit_arr)) for x in fit_arr]

  # create wheel
  accumulate_arr = []
  accumulated = 0
  for i in range(len(fit_arr)):
    accumulated += fit_arr[i]
    accumulate_arr.append(accumulated)

  # select new population
  selected = []

  for _ in range(final_size):
    randy = random.uniform(0,accumulated)
    index = bisect.bisect_left(accumulate_arr,randy)
    selected.append(individual_list[index])

  return selected

def mutation(individual_list:list[Individual],sigma,mutation_name):
  for i in individual_list:
    getattr(i,"mutation_"+mutation_name)(sigma)

def survival(individual_list,final_size):
  individual_list.sort(key=lambda x: x.getFitness())
  return individual_list[:final_size]

# ----------------------------------------------- #
# DE
# ----------------------------------------------- #

def de_rand_1_bin(ind_list):
  for i in range(0,len(ind_list)):
    valid_list = [other for other in ind_list if other != ind_list[i]]
    sam = random.sample(valid_list,3)
    ind_list[i] = ind_list[i].mut_cross_select_2(sam[0],sam[1],sam[2])
  return ind_list[:]

def de_rand_2_bin(ind_list):
  for i in range(0,len(ind_list)):
    valid_list = [other for other in ind_list if other != ind_list[i]]
    sam = random.sample(valid_list,5)
    ind_list[i] = ind_list[i].mut_cross_select_4(sam[0],sam[1],sam[2],sam[3],sam[4])
  return ind_list[:]

def de_best_1_bin(ind_list):
  for i in range(0,len(ind_list)):
    best = min(ind_list,key=lambda x: x.getFitness())
    valid_list = [other for other in ind_list if other != ind_list[i] and other != best]
    sam = random.sample(valid_list,2)
    ind_list[i] = ind_list[i].mut_cross_select_2(best,sam[0],sam[1])
  return ind_list[:]

def de_best_2_bin(ind_list):
  for i in range(0,len(ind_list)):
    best = min(ind_list,key=lambda x: x.getFitness())
    valid_list = [other for other in ind_list if other != ind_list[i] and other != best]
    sam = random.sample(valid_list,4)
    ind_list[i] = ind_list[i].mut_cross_select_4(best,sam[0],sam[1],sam[2],sam[3])
  return ind_list[:]

def de_current_to_best_1_bin(ind_list):
  for i in range(0,len(ind_list)):
    best = min(ind_list,key=lambda x: x.getFitness())
    valid_list = [other for other in ind_list if other != ind_list[i] and other != best]
    sam = random.sample(valid_list,2)
    ind_list[i] = ind_list[i].mut_cross_select_2(sam[0],best,sam[1])
  return ind_list[:]

def de_current_to_best_2_bin(ind_list):
  for i in range(0,len(ind_list)):
    best = min(ind_list,key=lambda x: x.getFitness())
    valid_list = [other for other in ind_list if other != ind_list[i] and other != best]
    sam = random.sample(valid_list,4)
    ind_list[i] = ind_list[i].mut_cross_select_4(sam[0],best,sam[1],sam[2],sam[3])
  return ind_list[:]


# ----------------------------------------------- #
# PSO
# ----------------------------------------------- #

def pso_2_bin(ind_list):
  for i in range(0,len(ind_list)):
    ind_list[i] = ind_list[i].cloud_particle_loop(ind_list)
  return ind_list[:]
