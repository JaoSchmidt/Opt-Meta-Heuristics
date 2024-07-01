import numpy as np
from abc import ABC, abstractmethod
import random
import sys

class Individual(ABC):
  def __init__(X):
    self.setPosition(X)

  @abstractmethod
  def _fitness_function(self,X):
    pass

  def getFitness(self):
    return self._current_min

  def _setFitness(self):
    self._current_min = self._fitness_function(self._X)

  def setPosition(self,X):
    self._X = X
    self._setFitness()

  def print(self):
    print([self._X,self._current_min])

  def to_dict(self):
    out = {}
    out["X"] = self._X
    out["Z"] = self._current_min
    return out

  def is_within_bounds(self, center=[0,0], bounds=[-5,5]):
    pos = self._X - np.array(center)
    return np.all(pos >= bounds[0]) and np.all(pos <= bounds[1])

class IndividualGA(Individual):
  def __init__(self,X,alpha):
    self.setPosition(X)
    self.alpha = alpha

  def recombination_average(self,other):
    rec = np.add(self._X,other._X)
    inst = type(self)(rec/2,self.alpha)
    return inst

  def mutation_creep(self,sigma):
    self._X += np.random.normal(0,sigma,size=len(self._X))
    self._setFitness()

  def mutation_gaussian(self, sigma):
    self._X = np.random.normal(self._X,sigma,size=len(self._X))
    self._setFitness()

  def recombination_geometric(self,other):
    # I'm not sure what to do here with negative values, I suppose this crossover shouldn't be used for this problem
    rec = np.sqrt(np.abs(np.multiply(self._X,other._X)))
    inst = type(self)(rec,self.alpha)
    return inst

  def recombination_blx_alpha(self,other):
    beta = random.uniform(0-self.alpha,1+self.alpha)
    rec = np.add(self._X,beta*np.add(-self._X,other._X))
    inst = type(self)(rec,self.alpha)
    return inst

  def recombination_blx_two_sons(self,other):
    beta = random.uniform(0,1)
    rec1 = beta*self._X
    rec2 = np.add(self._X,beta*np.add(other._X,-self._X))
    return [type(self)(rec1,self.alpha),type(self)(rec2,self.alpha)]

class IndividualDE(Individual):
  def __init__(self,X,R,Cr,min_b,diff):
    self.setPosition(X)
    self.__R = R
    self.__Cr = Cr
    self.__min_b = min_b
    self.__diff = diff

  def __recombination(self,mut_pos):
    dim = len(self._X)
    cross_points = np.random.rand(dim) < self.__Cr
    if not np.any(cross_points):
      cross_points[np.random.randint(0, dim)] = True
    son_pos = np.where(cross_points,mut_pos,self._X)
    #son_pos_denorm = self.__min_b + son_pos * self.__diff
    if self._fitness_function(son_pos) < self.getFitness(): # if created position is better
      return type(self)(son_pos,self.__R,self.__Cr,self.__min_b,self.__diff)
    else:
      return self
      #return type(self)(self._X,self.__R,self.__Cr)


  def mut_cross_select_4(self,base,other1,other2,other3,other4):
    rec1 = np.subtract(other1._X,other2._X)
    rec1 = rec1*self.__R
    rec2 = np.subtract(other3._X,other4._X)
    rec2 = rec2*self.__R
    mut_pos  = np.add(base._X,rec1,rec2)
    return self.__recombination(mut_pos)

  def mut_cross_select_2(self,base,other1,other2):
    mut_pos = base._X + (other1._X - other2._X)*self.__R
    return self.__recombination(mut_pos)

class IndividualPSO(Individual):
  gi = None
  def __init__(self,X,w,C1,C2,P=None,v=None):
    self.setPosition(X)
    self.__w = w
    self.__C1 = C1
    self.__C2 = C2
    if P is None:
      self.__P = X
    else:
      self.__P = P
    if v is None:
      self.__v = np.zeros(len(X))
    else:
      self.__v = v

  def get_data(self):
    out = {}
    out["X"] = self._X
    out["Z"] = self._current_min
    out["V"] = self.__v
    return out

  def cloud_particle_loop(self,ind_list, bounds, vbounds):
    # Local and global bests
    if self.getFitness() <= self._fitness_function(self.__P):
      self.__P = self._X
      if IndividualPSO.gi is None:
        IndividualPSO.gi = min(ind_list,key=lambda x: x.getFitness())
      if self.getFitness() <= IndividualPSO.gi.getFitness():
        IndividualPSO.gi = self
        return self

    # parameters
    r1 = np.random.random_sample(size=len(self._X))
    r2 = np.random.random_sample(size=len(self._X))
    param1 = (self.__P-self._X)*(self.__C1*r1)
    param2 = (IndividualPSO.gi._X - self._X)*(self.__C2*r2)

    # velocity
    if vbounds is None:
      self.__v = self.__v * self.__w + param1 + param2
    else:
      self.__v = np.clip(self.__v*self.__w + param1 + param2,vbounds[0],vbounds[1])

    # position
    if bounds is None:
      new_pos = self._X + self.__v
    else:
      new_pos = np.clip(self._X + self.__v,bounds[0],bounds[1])

    return type(self)(new_pos,self.__w,self.__C1,self.__C2,self.__P,self.__v)

class IndividualDEEPSO(Individual):
  def __init__(self,X,wi0,wa0,wc0,v,p):
    self.setPosition(X)
    self.__wi = wi0
    self.__wa = wa0
    self.__wc = wc0
    self.__P = p
    self.__v = v

  def mutation_w(self,w, tmut, wBounds):
    w = np.clip(w + tmut*np.random.normal(),wBounds[0],wBounds[1])
    return w

  def toJSON(self):
    return json.dumps(
      self,
      default=lambda o: o.__dict__,
      sort_keys=True,
      indent=4)

  def to_dict(self):
    out = {}
    out["X"] = self._X
    out["Z"] = self._current_min
    out["V"] = self.__v
    return out

  def print(self):
    out = {}
    out["X"] = self._X
    out["Z"] = self._current_min
    out["V"] = self.__v
    out["wi"] = self.__wi
    out["wa"] = self.__wa
    out["wc"] = self.__wc
    out["P-X"] = self.__P-self._X
    print(out)

  def rand_1(self,gb_wrapper,tmut, tcom, bounds=None, vBounds=None, wBounds=None):
    if self.getFitness() < self._fitness_function(self.__P):
      self.__P = self._X
      if self.getFitness() < gb_wrapper[0].getFitness():
        gb_wrapper[0] = self
        return self

    # if not self.is_within_bounds(center=[1,1],bounds=[-0.05,0.05]) and self.__temp > 60:
    #   self.print()

    C = np.random.random_sample(size=len(self._X))
    for i in range(0,len(C)):
      if C[i] < tcom:
        C[i] = 1
      else:
        C[i] = 0

    # Ws
    self.__wi = self.mutation_w(self.__wi,tmut, wBounds)
    self.__wa = self.mutation_w(self.__wa,tmut, wBounds)
    self.__wc = self.mutation_w(self.__wc,tmut, wBounds)

    # parameters
    param1 = self.__wa*(self.__P-self._X)
    param2 = self.__wc*C*(gb_wrapper[0]._X - self._X)

    # velocity
    self.__v = np.clip(self.__v*self.__wi + param1 + param2,*vBounds)
    # position
    new_pos = np.clip(self._X + self.__v,*bounds)

    return type(self)(new_pos,self.__wi,self.__wa,self.__wc,self.__v,self.__P)

class IndividualCDEEPSO(Individual):
  gi = None
  def __init__(self,X,wi0=0.5,wa0=0.5,wc0=0.5,v=None,p=None):
    self.setPosition(X)
    self.__wi = wi0
    self.__wa = wa0
    self.__wc = wc0
    self.__P = p
    self.__v = v

  def mutation_w(self,w, tmut):
    w = np.clip(w + tmut*np.random.normal(),0,2)
    return w

  def rand_1(self,ind_list, tmut, tcom, bounds=None, vBounds=None, wBounds=None):
    if IndividualCDEEPSO.gi is None:
      IndividualCDEEPSO.gi = min(ind_list,key=lambda x: x.getFitness())
    if self.getFitness() <= self._fitness_function(self.__P):
      self.__P = self._X
      if self.getFitness() < IndividualCDEEPSO.gi.getFitness():
        IndividualCDEEPSO.gi = self
        return self

    # if not self.is_within_bounds(center=[1,1],bounds=[-0.05,0.05]) and self.__temp > 60:
    #   self.print()

    C = np.random.random_sample(size=len(self._X))
    for i in range(0,len(C)):
      if C[i] < tcom:
        C[i] = 1
      else:
        C[i] = 0

    # Ws
    self.__wi = self.mutation_w(self.__wi,tmut, wBounds)
    self.__wa = self.mutation_w(self.__wa,tmut, wBounds)
    self.__wc = self.mutation_w(self.__wc,tmut, wBounds)

    # parameters
    param1 = self.__wa*(self.__P-self._X)
    param2 = self.__wc*C*(IndividualCDEEPSO.gi._X - self._X)

    # velocity
    if vBounds is None:
      self.__v = self.__v*self.__wi + param1 + param2
    else:
      self.__v = np.clip(self.__v*self.__wi + param1 + param2,vBounds[0],vBounds[1])

    # position
    if bounds is None:
      new_pos = self._X + self.__v
    else:
      new_pos = np.clip(self._X + self.__v,bounds[0],bounds[1])

    return type(self)(new_pos,self.__wi,self.__wa,self.__wc,self.__v,self.__P, temp=self.__temp+1)


