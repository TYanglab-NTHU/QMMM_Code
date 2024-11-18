# 18.11.2024
# diverse stress test
# addition of H atoms fixed (hopefully)

import sys                      # IO Basics
import glob                     # wild cards in file names
import os                       # access file system
import random                   # create random number
import time                     # gather timing info
import shutil                   # functions to handle files in disc

# Import OpenBabel to assist with atom classification
from openbabel import openbabel as ob           # basic OpenBabel

# Import my modules
sys.path.append('/dicos_ui_home/tlankau/QMMM_Code/Q19_CCDC')
import globals as     gb      # short for globals
import qmmm    as     qms     # short for qm/mm separation
from   qmmm    import printf
from   qmmm    import fprintf

# VERY IMPORTANT, initialize globals
gb.init()

# define vital variables
file_dir = "/dicos_ui_home/tlankau/QMMM_Work/Stress_04/Query/QRes-424847/Results"

def mol2_num_atoms(file_name):
  name=""
  anz=0
  f = open(file_name,"r")
  linelist = f.readlines()
  cnt=0
  for line in linelist:
    if "@<TRIPOS>MOLECULE" in line : break
    cnt += 1
  name = linelist[cnt+1].strip()
  anz = linelist[cnt+2].strip()
  anz = anz.split()
  anz = int(anz[0])
  return(name, anz)

# write the versions of the modules to output
gb.VerboseFlag = 1
if gb.VerboseFlag > 0:
  print("Versions used for thisQM/MM separation")
  print("QM/MM module:", qms.Version) 
  print("             ", qms.VersDir) 
  print("qlobal vars :",  gb.Version) 
  print("             ",  gb.VersDir) 
  print()

total_time = 0
# loop over all files, because the directory has the right number of files
job_list = glob.glob(file_dir+'/*.mol2')
job_list.sort()
stress_anz = len(job_list)
cnt = 1
for file in job_list:
  printf("%4i/%i  ", cnt, stress_anz)
  name, numat = mol2_num_atoms(file)
  printf("%-8s  (%3i)", name, numat)
  reread_flag=bool(False)

  ##############################################################################
  # Do the QMM/MM separation                                                   #
  ##############################################################################

  # set output verbosity
  gb.VerboseFlag = 0

  if gb.VerboseFlag==0:
    ob.obErrorLog.SetOutputLevel(0)
    
  # read input file (modified copy form Q19_CCDC/cmd_line.py)
  gb.mol, gb.obmol, aux = qms.read_input_file(file)
  inp_name_new = ".".join(file.split('.')[0:-1])+"_add.mol2"
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

  # set details for the QM/MM separation
  qms.set_conju_angle(0)  # request default value
  qms.set_metal_coor(-1)  # match it to reality
  # qms.toggle_H_removal()  # remove H atoms from the distatnt neighbors list
  if gb.VerboseFlag > 0:
    print('Parameter which can be changed by the user')
    print('Twist angle for conjugated chains', qms.get_conju_angle())
    print('Minimum metal coordiantion number', qms.get_metal_coor())
    print('Remove H atoms form candidates   ', qms.get_H_removal())
    print()

  # standard QM/MM separation (That's all folks)
  start_time = time.time()
  qms.std_qmmm_sep()
  end_time   = time.time()

  # write output file with the QM/MM separation data
  outfile = file[:-5]
  outfile += ".xyz"
  outfile = outfile.replace(file_dir, ".")
  stats = qms.write_output_file(outfile)

  for number in stats:
    printf("  %4i", number)
  
  ##############################################################################
  # Leave the QMM/MM separation                                                #
  ##############################################################################
   
  time_diff = end_time - start_time
  total_time += time_diff
  printf("  %5.1f", time_diff)
  
  # check for added H atoms
  if stats[0]!=numat:
    printf("  Attn: H atoms added?")
  
  # check for a reread with added H atoms
  if reread_flag:
    printf("  Attn: Reread input with H atoms!")

  # end line
  printf("\n")
  
  # increase job counter
  cnt += 1

  # emergency break for testing
  # exit()

# final printout and summary
printf("Avergae time per QM/MM separation %.1f\n", total_time/stress_anz)  