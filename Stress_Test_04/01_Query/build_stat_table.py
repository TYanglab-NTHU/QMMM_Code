# load modules for Python coding
import sys                      # IO Basics
import glob                     # wild cards in file names
import os                       # access file system
import math                     # mathematical  functions
import random                   # create random number

file = open('use_archive.log', 'r', encoding='UTF-8')
line = file.readline() # read the very first line to start the game
while (line): # fast forward to the critical data block
    if 'Pick random entries' in line:
        break
    line = file.readline()
#initialize a nested dictionary for counting coordination numbers
dict = {'cn1' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn2' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn3' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn4' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn5' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn6' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn7' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn8' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn9' : {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn10': {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn11': {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0},
        'cn12': {'Mn': 0, 'Fe': 0, 'Co': 0, 'Ni': 0, 'Cu': 0, 'Ag': 0}}
# count the coordination numbers for each metal
for n in range(0,1000,1):
    line = file.readline().strip()
    print(line)
    line=line.split()
    dict['cn'+str(line[4])][line[1]] += 1
file.close()
print(dict)
# write csv file
with open('qres-424847.csv', 'w') as f:
    f.write('cn,Mn,Fe,Co,Ni,Cu,Ag\n')
    for i in range(1,13,1):
        f.write(f'%i' % (i))
        for m in ['Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Ag']:
            # print('cn'+str(i), m)
            f.write(f',%i' % (dict['cn'+str(i)][m]))
        f.write('\n')
    f.close()