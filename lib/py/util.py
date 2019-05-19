import sys
import subprocess
import os
import time
from shutil import copyfile
from pathlib import Path
import numpy as np
from math import *
import os, errno, glob, shutil, json
from pprint import pprint

def teste():
	print('teste')
def call_subprocess(command, directory, s):
	subp = subprocess.Popen(command, cwd=directory, shell=s)
	subp.wait()

def update_dummy(colvar_dir, colvar_name_list, center_file, selection, stage):
	call_subprocess("env center_file='"+center_file+"' selection='"+selection+"' vmd -dispdev text -e "+sys_inf['location']+"/lib/tcl/get-center-mass.tcl", colvar_dir, True)
	
	centerFile = open(colvar_dir+"/center.tmp")
	center=""
	for line in centerFile:
		center=line
	centerFile.close()
	center=center.split(" ")

	for i in range(0,len(colvar_name_list)):
		lines = open(colvar_dir+"/"+colvar_name_list[i], "r").readlines()
		colv = open(colvar_dir+"/"+colvar_name_list[i], "w")
		update_dummy = 0
		z=center[2].strip()
		for line in lines:
			if ((stage=='equil') and "posit-prot" in line):
				update_dummy = 1

			elif (stage=='smd') and ("posit-XY-lig" in line or "posit-Z-lig" in line):
				update_dummy = 1
				z=str(float(center[2].strip())-4)

			if ("dummyatom" in line) and (update_dummy==1):
				line = "	dummyatom ("+center[0]+", "+center[1]+", "+z+") \n"
				update_dummy=0

			colv.write(line)

		colv.close()

	os.remove(colvar_dir+"/center.tmp")

def createDir(location):
	if not os.path.exists(location):
		os.makedirs(location)
#Copy the lines from a file to another file

def copyFileLines(fileFrom, fileTo):
	file = open(fileFrom)
	for line in file:
		fileTo.write(line)

def getEnergy(file, collum):
	energy = np.genfromtxt('../analysis/'+file, usecols=(collum)).transpose()
	return float(energy[len(energy)-1])

def copyAllFilesWith(source_dir, dest_dir, expression):
	files = glob.iglob(os.path.join(source_dir, expression))
	for file in files:
		if (os.path.isfile(file)):
			shutil.copy2(file, dest_dir)

def editPDB():
	with open('common/aligned.pdb') as pdb:
		with open('common/new_pdb.pdb', 'w') as new_pdb:
			for line in pdb: 
				if not ' A ' in line and 'ATOM' in line:
					new_pdb.write(line)

	with open('common/system.pdb') as pdb:
		with open('common/compare.pdb', 'w') as new_pdb:
			for line in pdb:
				if 'ATOM' in line and 'REMARK' not in line:
					if 'TIP3' in line:
						line = line.replace('TIP3', 'TIP ')
					new_pdb.write(line)
	i = 0
	with open('common/new_pdb.pdb') as new_pdb:
		with open('common/compare.pdb') as compare_pdb:
			with open('common/final_pdb.pdb', 'w') as final_pdb:
				new_pdb_lines = new_pdb.readlines()
				compare_pdb_lines =  compare_pdb.readlines()
				data = np.genfromtxt('common/new_pdb.pdb', usecols=(4), dtype='str')
				data2 = np.genfromtxt('common/compare.pdb', usecols=(4), dtype='str')
				for i in range(len(data)):
					if data[i] == data2[i]:
						final_pdb.write(new_pdb_lines[i].replace(' B ', ' A '))
					else:
						final_pdb.write(new_pdb_lines[i])

	#os.rename('common/final_pdb.pdb', 'common/system.pdb')
#def editConfigFile(file, positions, additions):
	