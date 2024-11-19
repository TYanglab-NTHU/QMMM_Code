import pandas as pd               # import the data
import seaborn as sns             # data visualization
from collections import Counter   # data countaine (storage)
import matplotlib.pyplot as plt   # plot the data
from matplotlib import pyplot as plt,ticker
import numpy as np                # numerical mathematics
from scipy import stats           # scientific mathematic algorithms

# read file
tot_at = []
time = []
with open('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/slurm-442293.dat') as file:
    for line in file:
      line = line.rstrip()
      line = line.split()
      # print(line)
      tot_at.append(float(line[-8]))
      time.append(float(line[-1]))

print('Basic stats')
print(f'atoms: [%i:%i]' % (min(tot_at), max(tot_at)))
print(f'time: [%.1f:%.1f]' % (min(time), max(time)))

data = {"total_at": tot_at, "time": time}
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(25, 250)
ax.set_ylim(0,  8)
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=50))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=25))
ax = sns.histplot(x=data['total_at'], y=data['time'], bins=50, cmap="winter", cbar=True, element="step", cbar_kws={'label': 'Count'})

# plt.xlabel(r'$\Delta E_f^{oxo} $ (kcal/mol)',size=16)
plt.xlabel('number of atoms',size=16)
plt.ylabel('time (sec)' ,size=16)

ax.grid(True, which='both')
cbar = ax.collections[0].colorbar
cbar.locator = ticker.MaxNLocator(integer=True)
cbar.update_ticks()

plt.tight_layout()
# plt.show()
plt.savefig('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/stress04_time_det.jpg', dpi=400)
