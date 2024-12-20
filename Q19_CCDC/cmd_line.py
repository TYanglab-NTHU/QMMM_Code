################################################################################
# 16.11.2024 Q19_CCDC
# - add version directory VersDir
################################################################################

# set version string
Version='cm19-20241116'
# set directory
VersDir='/dicos_ui_home/tlankau/QMMM_Code/Q19_CCDC'

# Import basic Python modules
import sys                      # IO Basics
import glob                     # wild cards in file names
import os                       # access file system
import math                     # mathematical  functions
import shutil                   # functions to handle files in disc

# Import CCDC modules (CSD Python API)
from ccdc          import io                    # read crystal structures
csd_reader = io.EntryReader('CSD')

import ccdc.search
from ccdc.search   import TextNumericSearch     # search by text or numbers
from ccdc.search   import SubstructureSearch    # search for substructures

from ccdc.molecule import Molecule              # Build a molecule
from ccdc.molecule import Atom                  # Atomic data and properties
from ccdc.molecule import Bond                  # Bond properties

# Import OpenBabel to assist with atom classification
from openbabel import openbabel as ob           # basic OpenBabel

# Import my modules
sys.path.append(VersDir)
import globals as     gb      # short for globals
import qmmm    as     qms     # short for qm/mm separation
from   qmmm    import printf
from   qmmm    import fprintf

################################################################################
# general purpose function                                                     #
# function to delete global variables to limit the scope of these variables    #
# input  vlist  a list with the names (strings) of the variables to be         #
#               deleted.                                                       #
# output anz    integer with the number of deleted variables                   #
################################################################################

def clean_glob_var(vlist):
  if "gb" not in globals():
    print("Global variables not initialized")
    exit()
  anz = 0
  g = globals()
  for var in vlist:
    if var in globals():
      if gb.VerboseFlag==2: printf("%s in globals\n", var)
      anz += 1
      del g[var]
    else:
      if gb.VerboseFlag==2: printf("%s NOT in globals\n", var)
  if gb.VerboseFlag==2: printf("%i global variables deleted\n", anz)
  return(anz)

################################################################################

# VERY IMPORTANT, initialize globals
gb.init()

# Managing the cmd line is not part of the Python import
my_arglist = sys.argv.copy() # get command line argument
my_arglist.pop(0) # remove the command name

# test whether any arguments have been given
if len(my_arglist)==0:
  printf("bad command line parameter\n")
  printf("use %s [-v 0,1,2] file name\n", sys.argv[0])
  exit()

# look for optional verbose parameter
argpos = -1
for argcnt, my_arg in enumerate(my_arglist):
  if my_arg == "-v":
    argpos = argcnt
    break
my_arglist.pop(argpos)
my_arg = my_arglist.pop(argpos)
if my_arg in ["0", "1", "2"]:
  gb.VerboseFlag = int(my_arg)
else:
  printf("bad command line parameter\n")
  printf("use %s [-v 0,1,2] file name\n", sys.argv[0])
  exit()

# the last surviving argument is the file name
if len(my_arglist) != 1:
    printf("bad command line parameter\n")
    printf("use %s [-v 0,1,2] file name\n", sys.argv[0])
    exit()
inp_name = my_arglist[0]

# add version numbers to the output
if gb.VerboseFlag > 0:
  print("Versions used for thisQM/MM separation")
  print("cmd line    :",     Version)
  print("             ",     VersDir)
  print("QM/MM module:", qms.Version) 
  print("             ", qms.VersDir) 
  print("qlobal vars :" ,  gb.Version) 
  print("             " ,  gb.VersDir) 
  print()

if gb.VerboseFlag > 0:
  printf("Summarize command line parameter\n")
  printf("  VerboseFlag = %i", gb.VerboseFlag)
  if gb.VerboseFlag == 1:
    printf(" (default or cmd line)\n")
  else:
    printf("\n")
  printf("  Input File  = %s\n", inp_name)

# delete variables I don't need anay more
clean_glob_var(['my_arg', 'my_arglist', 'argpos', 'argcnt'])

# turn of OpenBabel warnings for no verbose runs
if gb.VerboseFlag==0:
  ob.obErrorLog.SetOutputLevel(0)

# clean up old files
if gb.VerboseFlag > 0: printf("Clean up old files\n")
for file in glob.glob("stp*xyz"):
  os.remove(file)
if os.path.exists("./combi.xyz"): os.remove("./combi.xyz")

################################################################################
# This is the critical part of the QM/MM separation and can be copied into
# other Python scripts
################################################################################

# read input file
gb.mol, gb.obmol, aux = qms.read_input_file(inp_name)
inp_name_new = ".".join(inp_name.split('.')[0:-1])+"_add.mol2"
if gb.mol == None and gb.obmol == None:
  if gb.VerboseFlag>0:
    print("  The addition of missing H atoms failed.")
    print(f"  Create new input file %s" % (inp_name_new))
  try:
    shutil.move(aux, inp_name_new)
  except:
    print(f"  Copy of aux_add_H.mol2 to %s failed" % (inp_name_new))
    exit()
  if gb.VerboseFlag>0:
    print("  Reset variables and try try to read", inp_name_new)
  VerboseFlag_old = gb.VerboseFlag
  del gb.mol, gb.obmol, gb.qm, gb.mm, gb.dnts
  del gb.VerboseFlag, gb.conju_twist_angle, gb.met_min_lig_num, gb.del_H_from_list
  gb.init()
  gb.VerboseFlag = VerboseFlag_old
  del VerboseFlag_old
  reread_flag=bool(True)
  gb.mol, gb.obmol, aux = qms.read_input_file(inp_name_new)
  if gb.mol == None and gb.obmol == None:
    print("Something is still terribly wrong with the additional H atoms")
    exit()
if os.path.exists(aux):
  shutil.move(aux, inp_name_new)

if bool(False):
  gb.mol, gb.obmol = qms.read_input_file(inp_name)
  if gb.mol == None and gb.obmol == None:
    inp_name_new = ".".join(inp_name.split('.')[0:-1])+"_add.mol2"
    if gb.VerboseFlag>0:
      print("  The addition of missing H atoms failed.")
      print(f"  Create new input file %s." % (inp_name_new))
    try:
      shutil.copyfile("./aux_add_H.mol2", "./"+inp_name_new)
    except:
      print(f"  Copy of aux_add_H.mol2 to %s failed" % (inp_name_new))
      exit()
    if gb.VerboseFlag>0:
      print("  Reset variables and try try to read", inp_name_new)
    VerboseFlag_old = gb.VerboseFlag
    del gb.mol, gb.obmol, gb.qm, gb.mm, gb.dnts
    del gb.VerboseFlag, gb.conju_twist_angle, gb.met_min_lig_num, gb.del_H_from_list
    gb.init()
    gb.VerboseFlag = VerboseFlag_old
    del VerboseFlag_old
    gb.mol, gb.obmol = qms.read_input_file(inp_name_new)
    if gb.mol == None and gb.obmol == None:
      print("Something is still terribly wrong with the additional H atoms")
      exit()

# optional part ofthe setup
if gb.VerboseFlag>0: print()
# modification of the default settings for the QM/MM separation
# set the twist angle for conjugated chains
# -1: turn the check for twisted chains off
#  0: set the default value of 30 deg
qms.set_conju_angle(0) # request default value
# set the minimum coordination number for metal atoms
# -1: turn the check for distant neighbors off
#  0: set the default value of 6 (octahedral coordination)
qms.set_metal_coor(3)  # match it to reality
# toggle the removal of H atoms from the candidate list
# qms.toggle_H_removal()
# verify the changed settings
if gb.VerboseFlag > 0:
  print('Parameter which can be changed by the user')
  print('Twist angle for conjugated chains', qms.get_conju_angle())
  print('Minimum metal coordiantion number', qms.get_metal_coor())
  print('Remove H atoms form candidates   ', qms.get_H_removal())

# standard QM/MM separation (deviation from the old code)
qms.std_qmmm_sep()

# write output file with the QM/MM separation data
stats = qms.write_output_file("combi.xyz")
if gb.VerboseFlag>0:
  print("List with a summary of the results", stats)

# end the code
exit()