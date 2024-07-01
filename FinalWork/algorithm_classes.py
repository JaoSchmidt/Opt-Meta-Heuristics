import numpy as np
import random
import sys
import os
from abc import ABC, abstractmethod

# ----------------------------------------------- #
# Algorithm Loop abstract
# ----------------------------------------------- #

class AlgorithmLoop(ABC):
  def __init__(self,title):
    self.__title = title

  @abstractmethod
  def test_nd_write_file(self, coordinates, IndividualClass, test_num=-1):
    pass

  def get_description():
    return self.__title

# ----------------------------------------------- #
# DEEPSO
# ----------------------------------------------- #

class LoopDEEPSO(AlgorithmLoop):
  def __init__(self,title,experiment_name,position_bounds,
               population_size=100,max_it=100,tcom=0.5,tmut=0.1,velocity_bounds=None,
               w_bounds=None,wi_initial=0.5,wa_initial=0.5,wc_initial=0.5):
    super().__init__(title)
    self.__title = title
    self.__max_it = max_it
    self.__wi0 = wi_initial
    self.__wa0 = wa_initial
    self.__wc0 = wc_initial
    self.__tmut = tmut
    self.__tcom = tcom

    # set bounds, if none, set max
    max_bound = [-sys.maxsize,sys.maxsize]
    self.__pb = position_bounds if position_bounds is not None else max_bound
    self.__vb = velocity_bounds if velocity_bounds is not None else max_bound
    self.__wb = w_bounds if w_bounds is not None else max_bound

    # setting the correct function
    match experiment_name:
      case "deepso_rand_1":
        fun = self.__deepso_rand_1
      case _:
        raise Exception("Unkown experiment name")
    self.__test_function = fun

  def test_nd_write_file(self,coordinates, IndividualClass, test_num=-1):
    generation_data = []
    population = [
        IndividualClass(coord,wi0=self.__wi0,wa0=self.__wa0,wc0=self.__wc0,
                        v=np.zeros(len(coord)),p=coord)
        for coord in coordinates
        ]

    global_best=min(population,key=lambda x: x.getFitness())
    gb_wrapper = [global_best]
    for gen_number in range(0,self.__max_it):
      generation_data.append(population)
      population = self.__test_function(population, gb_wrapper)
    return generation_data

  def __deepso_rand_1(self,ind_list, gb):
    new_generation = []
    for i in range(0,len(ind_list)):
      new_generation.append(ind_list[i].rand_1(gb, self.__tmut, self.__tcom,bounds=self.__pb, vBounds=self.__vb, wBounds=self.__wb))
    return new_generation

  def get_description(self):
    return self.__title+", tcom="+str(self.__tcom)+", tmut="+str(self.__tmut)+", wa0="+str(self.__wa0)+", wi0="+str(self.__wi0)+", wc0="+str(self.__wc0)
