import pandas as pd               # import the data
import seaborn as sns             # data visualization
from collections import Counter   # data countaine (storage)
import matplotlib.pyplot as plt   # plot the data
from matplotlib import pyplot as plt,ticker
import numpy as np                # numerical mathematics
from scipy import stats           # scientific mathematic algorithms
import pickle                     # read python objects from disk

# read the dictionary directly
del_data = []
with open('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/link_dict.pkl', 'rb') as fp:
    data = pickle.load(fp)
    print('Dictionary read')
    print(data)
# remove small contibutions
print('All  links', len(data))
for link in data:
    if data[link] < 5:
        del_data.append(link)
for link in del_data:
    del data[link]
print('Clean links', len(data))

# translate dictionary into lists for the plot
bond = list(data.keys())
count = list(data.values())
link_num = 0
for cnt in count:
    link_num += cnt

# create a plot to work on
fig, ax = plt.subplots(figsize=(10, 15))

# create a title for the plot
plt.title("QM-MM bonds ordered by appearance (>=5)", size=20)
plt.ylabel("bond type",size=20)
plt.xlabel("No. of bonds observerd",size=20)
plt.rcParams['font.size'] = 12

# add info
plt.text(1240, 37, "1000 cluster\n"+str(link_num)+" QM-MM bonds\n", size=12)

# creating the bar plot
plt.barh(bond, count, height=0.75)

plt.tight_layout()
# plt.show()
plt.savefig('/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Stats/stress04_link_min5.jpg', dpi=400)
