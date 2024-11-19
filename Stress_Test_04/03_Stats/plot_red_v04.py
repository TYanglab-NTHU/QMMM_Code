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
mm_at  = []
red    = []
print('Reduction lower than 5%')
with open('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/slurm-442293.dat') as file:
    for line in file:
      line = line.rstrip()
      line = line.split()
      x = int(line[-8])
      tot_at.append(x)
      y = int(line[-7])
      qm_at.append(y)
      z = int(line[-6])
      mm_at.append(z)
      red.append(z/x*100.0)
      if z/x*100.0 <= 5.0:
         print(line[1])
      # print(line)
      # print(x, y, z, z/x*100.0)
      # exit()

print()
print('Basic stats')
print(f'all atoms : [%i:%i]' % (min(tot_at), max(tot_at)))
print(f'QM atoms  : [%i:%i]' % (min(qm_at), max(qm_at)))
print(f'MM atoms  : [%i:%i]' % (min(mm_at), max(mm_at)))
print(f'reduction : [%4.1f:%4.1f]' % (min(red), max(red)))

# create a dictionary with all data to be plotted
data = {"tot": tot_at, "red": red}

# create a plot to work on
fig, ax = plt.subplots(figsize=(8, 6))

# create a title for the plot
plt.title("Reduction of QM atoms", size=20)

# define the label of the axes
plt.xlabel('number of atoms',size=16)
plt.ylabel('reduction of QM atoms (%)' ,size=16)

# define the axises for the plot
ax.set_xlim(25, 250)                                           # range of the y-axis
ax.set_ylim( 0, 100)                                           # range of the x-axis
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=50))    # x-axis major ticks
ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=25))    # x-axis minor ticks
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=25))    # y-axis major ticks
ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=12.5))  # y-axis minor ticks

# insert a text box with the equation for the reduction
plt.text(175, 5, r"red. = $\dfrac{N_{MM}}{N_{tot}} \times 100 \%$", size=12)

# create histogrm for the density
ax = sns.histplot(x=data['tot'], y=data['red'], bins=50, cmap="winter", cbar=True, element="step", cbar_kws={'label': 'Count'})

plt.tight_layout()
# plt.show()
plt.savefig('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/stress04_reduction.jpg', dpi=400)
