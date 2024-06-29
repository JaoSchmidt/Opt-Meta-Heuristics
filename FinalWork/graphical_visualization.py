import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PathCollection
from matplotlib import rcParams
from IPython.display import clear_output

def contour_over_population(generation_data,title,ff,bounds,save_path='animation.mp4'):
  rcParams['animation.convert_path'] = r'/usr/bin/convert'
  fig, ax = plt.subplots(figsize=(10, 10))


  # # generate countour
  x = np.linspace(bounds[0]*1.2,bounds[1]*1.2,200)
  y = np.linspace(bounds[0]*1.2,bounds[1]*1.2,200)
  contour_X, contour_Y = np.meshgrid(x,y)
  contour_Z = ff((contour_X,contour_Y))
  ax.contour(contour_X, contour_Y, contour_Z, levels=80, cmap='rainbow', alpha=0.4,zorder=0)
  rec = patches.Rectangle((bounds[0], bounds[0]), bounds[1]*2, bounds[1]*2, linewidth=1, edgecolor='r', facecolor='none')
  ax.add_patch(rec)
  ax.autoscale(False) # To avoid that the scatter changes limits

  ax.set_xlabel('x')
  ax.set_ylabel('y')


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
    x = [p.get_data()["X"][0] for p in generation]
    y = [p.get_data()["X"][1] for p in generation]
    ax.scatter(x, y, marker='o', zorder=100, color="red")

    # velocity
    for p in generation:
      pos = p.get_data()["X"]
      vel = p.get_data()["V"]
      ax.arrow(pos[0], pos[1], vel[0], vel[1], head_width=0.05, head_length=0.1, fc='blue', ec='blue')

  ani = FuncAnimation(fig,update, frames=len(generation_data),repeat=True, interval=50)
  ani.save(save_path, writer='ffmpeg',fps=1)
  fig.clear()

def get_last_best_ind(generation_data,*args):
  last_gen = generation_data[len(generation_data)-1]
  best_ind = min(last_gen,key=lambda x:x.getFitness())
  return [args,*best_ind.get_data()]

def store_average_fitness(generation_data,final_fitness_table,scenario_name):
  mini = final_fitness_table["mini"][scenario_name]
  mean = final_fitness_table["mean"][scenario_name]
  for i,generation in enumerate(generation_data):
    if (len(mini) < len(generation_data)):
      mini.append(min(generation,key=lambda x: x.getFitness()).getFitness())
      mean.append(sum([ind.getFitness() for ind in generation])/len(generation))
    else:
      mini[i] += min(generation,key=lambda x: x.getFitness()).getFitness()
      mean[i] += sum([ind.getFitness() for ind in generation])/len(generation)

def store_fitness_pymoo(generation_data,final_fitness_table,scenario_name,num_tests):
  for i,generation in enumerate(generation_data):
    if (len(final_fitness_table["mini"][scenario_name]) < len(generation_data)):
      final_fitness_table["mini"][scenario_name] = [x for x in generation_data["min"]]
      final_fitness_table["mean"][scenario_name] = [x for x in generation_data["avg"]]
    else:
      for x in generation_data["min"]:
        final_fitness_table["mini"][scenario_name][i] += x
      for x in generation_data["avg"]:
        final_fitness_table["mean"][scenario_name][i] += x

def store_fitness_pyswarm(generation_pos,fitness_fn,final_fitness_table,scenario_name,num_tests):
  for i,generation in enumerate(generation_pos):
    if len(final_fitness_table["mini"][scenario_name]) < len(generation_pos):
      final_fitness_table["mini"][scenario_name].append(min([fitness_fn(x) for x in generation]))
      final_fitness_table["mean"][scenario_name].append(sum([fitness_fn(x) for x in generation]))
    else:
      final_fitness_table["mini"][scenario_name][i] = (min([fitness_fn(x) for x in generation]))
      final_fitness_table["mean"][scenario_name][i] = (sum([fitness_fn(x) for x in generation]))

def plot_fitness_over_generation(final_fitness_table, num_tests):

    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    for title, values in final_fitness_table["mini"].items():
      axs[0].plot(list(range(0,len(values))), [v/num_tests for v in values], label=title, linestyle='-')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].set_title("Minimum Fit x Gen")
    axs[0].set_yscale('log')

    for title, values in final_fitness_table["mean"].items():
      axs[1].plot(list(range(0,len(values))), [v/num_tests for v in values], label=title, linestyle='-')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].set_title("Avg Fit x Gen")
    axs[1].set_yscale('log')

    plt.show()
