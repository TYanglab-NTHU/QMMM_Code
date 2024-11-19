import pandas as pd               # import the data
import seaborn as sns             # data visualization
from collections import Counter   # data countaine (storage)
import matplotlib.pyplot as plt   # plot the data
from matplotlib import pyplot as plt,ticker
import numpy as np                # numerical mathematics
from scipy import stats           # scientific mathematic algorithms

# read file (later dodes will create cvs files directly)
tot_at = []
qm_at  = []
red    = []
print('More than 100 quantum atoms')
with open('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/slurm-442293.dat') as file:
    for line in file:
      line = line.rstrip()
      line = line.split()
      x = int(line[-8])
      tot_at.append(x)
      y = int(line[-7])
      if y>=100:
         print(line[1])
      qm_at.append(y)
      red.append(y/x*100.0)
      # print(line)
      # print(x, y)
      # exit()

print()
print('Basic stats')
print(f'all atoms : [%i:%i]' % (min(tot_at), max(tot_at)))
print(f'QM atoms  : [%i:%i]' % (min(qm_at), max(qm_at)))
print(f'reduction : [%4.1f:%4.1f]' % (min(red), max(red)))

# create a dictionary with all data to be plotted
data = {"tot": tot_at, "qm": qm_at}

# create a plot to work on
fig, ax = plt.subplots(figsize=(8, 6))

# create a title for the plot
plt.title("Number of Quantum Atoms", size=20)

# define the label of the axes
plt.xlabel('all atoms',size=16)
plt.ylabel('quantum atoms' ,size=16)

# define the axises for the plot
ax.set_xlim(25, 250)                                           # range of the y-axis
ax.set_ylim( 0, 120)                                           # range of the x-axis
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=50))    # x-axis major ticks
ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=25))    # x-axis minor ticks
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=40))    # y-axis major ticks
ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=20))    # y-axis minor ticks

# create histogrm for the density
ax = sns.histplot(x=data['tot'], y=data['qm'], bins=50, cmap="winter", cbar=True, element="step", cbar_kws={'label': 'Count'})

plt.tight_layout()
# plt.show()
plt.savefig('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/stress04_qmat.jpg', dpi=400)
