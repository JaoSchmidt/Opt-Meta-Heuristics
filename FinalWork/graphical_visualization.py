import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PathCollection
from matplotlib import rcParams
from IPython.display import clear_output
from individual_class import Individual

# ----------------------------------------------- #
# Graphics General
# ----------------------------------------------- #

def plot_fitness_over_tests(table_test: dict, legend=False, ):
  fig, axs = plt.subplots(1,2,figsize=(16, 6))

  for title,values in table_test.items():
    axs[0].plot(list(range(0,len(values['mini']))), values['mini'], label=title, linestyle='-')
    axs[1].plot(list(range(0,len(values['mean']))), values['mean'], label=title, linestyle='-')
  axs[0].legend()
  axs[0].grid(True)
  axs[0].set_title("Minimum Fitness of all tests")
  axs[0].set_yscale('log')

  axs[1].legend()
  axs[1].grid(True)
  axs[1].set_title("Average Fitness of all tests")
  axs[1].set_yscale('log')
  table_test.clear()


def plot_fitness_over_scenarios(table_scenario: dict, scenario_name: str):
  fig, axs = plt.subplots(2, 2, figsize=(16, 12))
  for title, values in table_scenario.items():
    axs[0,0].plot(list(range(0,len(values["mini"]))), values["mini"], label=title, linestyle='-')
  axs[0,0].legend()
  axs[0,0].grid(True)
  axs[0,0].set_title("Minimum Fitness (Average of all tests)")
  axs[0,0].set_ylabel('fitness')
  axs[0,0].set_yscale('log')

  for title, values in table_scenario.items():
    axs[0,1].plot(list(range(0,len(values["mean"]))), values["mean"], label=title, linestyle='-')
  axs[0,1].legend()
  axs[0,1].grid(True)
  axs[0,1].set_title("Average Fitness (Average of all tests)")
  axs[0,1].set_ylabel('fitness')
  axs[0,1].set_yscale('log')

  # for title, values in table_scenario.items():
  axs[1,0].boxplot([table_scenario[s]["fitness_last"] for s in table_scenario], labels=[s for s in table_scenario], showfliers=True)
  axs[1,0].set_ylabel('fitness')
  axs[1,0].set_xlabel('scenario')
  axs[1,0].set_yscale('log')
  axs[1,0].set_title('Last Gen Fitness (all tests)')

  # print boxplot of positions for last scenario only
  values = np.array(table_scenario[scenario_name]["position_last"])
  num_dimensions = values.shape[1]
  boxplot_data = [values[:, d] for d in range(num_dimensions)]
  # print(boxplot_data)
  if num_dimensions == 2:
    axs[1,1].boxplot(boxplot_data, labels=["X","Y"], showfliers=True)
  else:
    axs[1,1].boxplot(boxplot_data, labels=[f'd{i+1}' for i in range(num_dimensions)], showfliers=True)
  axs[1,1].set_ylabel('position')
  axs[1,1].set_xlabel('dimensions')
  axs[1,1].set_title('Positions for scenario "'+scenario_name+'"')
  plt.show()

# ----------------------------------------------- #
# Animated
# ----------------------------------------------- #

def contour_over_population(generation_data,title,bounds,save_path='animation.mp4',max_it=10000):
  rcParams['animation.convert_path'] = r'/usr/bin/convert'
  fig, ax = plt.subplots(figsize=(10, 10))
  one_sample = generation_data[0][0]

  # -------------------------------------------------------------- #
  # generate countour
  x = np.linspace(bounds[0]*1.2,bounds[1]*1.2,200)
  y = np.linspace(bounds[0]*1.2,bounds[1]*1.2,200)
  contour_X, contour_Y = np.meshgrid(x,y)
  contour_Z = one_sample._fitness_function(np.array([contour_X, contour_Y]))
  ax.contour(contour_X, contour_Y, contour_Z, levels=80, cmap='rainbow', alpha=0.4,zorder=0)
  rec = patches.Rectangle((bounds[0], bounds[0]), bounds[1]*2, bounds[1]*2, linewidth=1, edgecolor='r', facecolor='none')
  ax.add_patch(rec)
  ax.autoscale(False) # To avoid that the scatter changes limits

  ax.set_xlabel('x')
  ax.set_ylabel('y')

  # -------------------------------------------------------------- #
  # update function
  def update(frame):
    for s in ax.collections:
      if isinstance(s, PathCollection):
        s.remove()

    for s in ax.patches:
      if isinstance(s, patches.FancyArrow):
        s.remove()

    generation = generation_data[frame]
    ax.set_title("Generation {} ".format(frame) + title)

    # position
    x = [p.to_dict()["X"][0] for p in generation]
    y = [p.to_dict()["X"][1] for p in generation]
    ax.scatter(x, y, marker='o', zorder=100, color="red")

    # velocity
    for p in generation:
      pos = p.to_dict()["X"]
      vel = p.to_dict()["V"]
      ax.arrow(pos[0], pos[1], vel[0], vel[1], head_width=0.05, head_length=0.1, fc='blue', ec='blue')

  frames = len(generation_data) if len(generation_data) < max_it else max_it
  ani = FuncAnimation(fig,update,repeat=True, interval=25, frames=frames)
  ani.save(save_path, writer='ffmpeg',fps=1)
  fig.clear()

# ----------------------------------------------- #
# Collectors
# ----------------------------------------------- #

def collect_data_on_scenario(table_scenario: dict, num_tests):
  table_scenario["mini"] = [m/num_tests for m in table_scenario["mini"]]
  table_scenario["mean"] = [m/num_tests for m in table_scenario["mini"]]

def collect_data_on_tests(scenario_data,table_scenario: dict, table_test = None, test_num=-1):
  mini = table_scenario["mini"]
  mean = table_scenario["mean"]
  fitness_last = table_scenario["fitness_last"]
  position_last = table_scenario["position_last"]

  # getting mean and minimum of each generation
  if not mini: # if it's the first time collecting data, then append data
    for generation in scenario_data:
      mini.append(min(generation,key=lambda x: x.getFitness()).getFitness())
      mean.append(sum([ind.getFitness() for ind in generation])/len(generation))
  else: # else sum with existing data
    for i,generation in enumerate(scenario_data):
      mini[i] += min(generation,key=lambda x: x.getFitness()).getFitness()
      mean[i] += sum([ind.getFitness() for ind in generation])/len(generation)

  # get fitness and position of last generation
  last_gen = scenario_data[len(scenario_data)-1]
  for ind in last_gen: # for all Individuals of the last generation
    d = ind.to_dict()
    fitness_last.append(d["Z"]) # collect their fitness
    position_last.append(d["X"]) # and collect their positions

  # here, I collect stuff to be used to visualize all tests, instead of the scenario
  if table_test is not None and test_num != -1:
    table_test["test "+str(test_num)] = {}
    table_test["test "+str(test_num)]["mini"] = []
    table_test["test "+str(test_num)]["mean"] = []
    for generation in scenario_data:
      table_test["test "+str(test_num)]["mini"].append(min(generation,key=lambda x: x.getFitness()).getFitness())
      table_test["test "+str(test_num)]["mean"].append(sum([ind.getFitness() for ind in generation])/len(generation))


# ----------------------------------------------- #
# Library collectors
# ----------------------------------------------- #

def store_fitness_pymoo(generation_data,final_fitness_table,scenario_name,num_tests):
  if (len(final_fitness_table["mini"][scenario_name]) < len(generation_data)):
    for i,generation in enumerate(generation_data):
      final_fitness_table["mini"][scenario_name] = [x for x in generation_data["min"]]
      final_fitness_table["mean"][scenario_name] = [x for x in generation_data["avg"]]
  else:
    for i,generation in enumerate(generation_data):
      for x in generation_data["min"]:
        final_fitness_table["mini"][scenario_name][i] += x
      for x in generation_data["avg"]:
        final_fitness_table["mean"][scenario_name][i] += x

def store_fitness_pyswarm(generation_pos,fitness_fn,final_fitness_table,scenario_name,num_tests):
  if len(final_fitness_table["mini"][scenario_name]) < len(generation_pos):
    for i,generation in enumerate(generation_pos):
      final_fitness_table["mini"][scenario_name].append(min([fitness_fn(x) for x in generation]))
      final_fitness_table["mean"][scenario_name].append(sum([fitness_fn(x) for x in generation]))
  else:
    for i,generation in enumerate(generation_pos):
      final_fitness_table["mini"][scenario_name][i] = (min([fitness_fn(x) for x in generation]))
      final_fitness_table["mean"][scenario_name][i] = (sum([fitness_fn(x) for x in generation]))

