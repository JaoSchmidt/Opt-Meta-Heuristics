import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def contour_over_population(generation_data,title,ff,map_size):

  x = np.linspace(-map_size*1.2/2,map_size*1.2/2,200)
  y = np.linspace(-map_size*1.2/2,map_size*1.2/2,200)
  contour_X, contour_Y = np.meshgrid(x,y)
  contour_Z = ff((contour_X,contour_Y))

  _, ax = plt.subplots(figsize=(10, 10))
  ax.contour(contour_X, contour_Y, contour_Z, levels=80, cmap='rainbow', alpha=0.4,zorder=0)
  rec = patches.Rectangle((-map_size/2, -map_size/2), map_size, map_size, linewidth=1, edgecolor='r', facecolor='none')
  ax.add_patch(rec)
  ax.autoscale(False) # To avoid that the scatter changes limits
  for i, generation in enumerate(generation_data):
    redness = i/len(generation_data)
    alpha = 0.2 + 0.8*i/len(generation_data)
    x = [p.get_data()[0] for p in generation]
    y = [p.get_data()[1] for p in generation]
    ax.scatter(x,y, marker='o', color=(redness,0.0,0.0),alpha=alpha,zorder=100)
  plt.title(title)
  plt.xlabel('x')
  plt.ylabel('y')
  plt.show()

def get_last_best_ind(generation_data,*args):
  last_gen = generation_data[len(generation_data)-1]
  best_ind = min(last_gen,key=lambda x:x.getFitness())
  return [args,*best_ind.get_data()]

def store_average_fitness(generation_data,final_fitness_table,scenario_name,num_test):
  mini = final_fitness_table["mini"][scenario_name]
  mean = final_fitness_table["mean"][scenario_name]
  for i,generation in enumerate(generation_data):
    #print(generation)
    if (len(mini) < len(generation_data)):
      mini.append(min(generation,key=lambda x: x.getFitness()).getFitness()/num_test)
      mean.append(sum([ind.getFitness() for ind in generation])/(len(generation)*num_test))
    else:
      mini[i] += min(generation,key=lambda x: x.getFitness()).getFitness()/num_test
      mean[i] += sum([ind.getFitness() for ind in generation])/(len(generation)*num_test)

def store_fitness_pymoo(generation_data,final_fitness_table,scenario_name,num_tests):
  for i,generation in enumerate(generation_data):
    if (len(final_fitness_table["mini"][scenario_name]) < len(generation_data)):
      final_fitness_table["mini"][scenario_name] = [x/num_tests for x in generation_data["min"]]
      final_fitness_table["mean"][scenario_name] = [x/num_tests for x in generation_data["avg"]]
    else:
      for x in generation_data["min"]:
        final_fitness_table["mini"][scenario_name][i] += x/num_tests
      for x in generation_data["avg"]:
        final_fitness_table["mini"][scenario_name][i] += x/num_tests

def plot_fitness_over_generation(final_fitness_table):

    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
   
    for title, values in final_fitness_table["mini"].items():
      axs[0].plot(list(range(0,len(values))), values, label=title, linestyle='-')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].set_title("Minimum Fit x Gen")
    axs[0].set_yscale('log')

    for title, values in final_fitness_table["mean"].items():
      axs[1].plot(list(range(0,len(values))), values, label=title, linestyle='-')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].set_title("Avg Fit x Gen")
    axs[1].set_yscale('log')

    plt.show()
