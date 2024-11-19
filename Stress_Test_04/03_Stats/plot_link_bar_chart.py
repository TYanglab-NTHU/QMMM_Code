import pandas as pd               # import the data
import seaborn as sns             # data visualization
from collections import Counter   # data countaine (storage)
import matplotlib.pyplot as plt   # plot the data
from matplotlib import pyplot as plt,ticker
import numpy as np                # numerical mathematics
from scipy import stats           # scientific mathematic algorithms
import pickle                     # read python objects from disk

# read the dictionary directly
with open('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/link_dict.pkl', 'rb') as fp:
    data = pickle.load(fp)
    print('Dictionary read')
    print(data)
# transform data
bond = list(data.keys())
count = list(data.values())

# create a plot to work on
fig, ax = plt.subplots(figsize=(10, 15))

# create a title for the plot
plt.title("QM-MM bonds ordered by appearance", size=20)
plt.ylabel("bond type",size=16)
plt.xlabel("No. of bonds observerd",size=20)
plt.rcParams['font.size'] = 12

# add info
plt.text(1250, 78, "1000 cluster\n5353 QM-MM bonds", size=12)

# creating the bar plot
plt.barh(bond, count, height=0.75)

plt.tight_layout()
# plt.show()
plt.savefig('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/stress04_link_analysis.jpg', dpi=400)
