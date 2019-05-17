import os
import shutil
from lib.py import util

def splitChains(pdb_file, protein_selection, ligand_selection, location, common_location):
	command = "env pdb_file='%s' protein_selection='%s' ligand_selection='%s' vmd -dispdev text -e %s/lib/tcl/split.tcl" % (pdb_file, ligand_selection, protein_selection, location)
	util.call_subprocess(command, common_location, True)

def generatePSF(parameters, sys_name, location, common_location):
	parameters = parameters.split(',')

	psf_tcl = open('lib/tcl/psf.tcl','r').readlines()

	for x in range(0, len(parameters)):
		psf_tcl.insert(x+1,'topology '+parameters[x].strip()+"\n")

	psf_tcl_tmp = open('lib/tcl/psf.tmp.tcl','w')
	psf_tcl = ''.join(psf_tcl)
	psf_tcl_tmp.write(psf_tcl)
	psf_tcl_tmp.close()

	command = "env sys_name='%s' vmd -dispdev text -e %s/lib/tcl/psf.tmp.tcl" % (sys_name, location)
	util.call_subprocess(command, common_location, True)

	os.remove('lib/tcl/psf.tmp.tcl')

def solvate(min_box, max_box, location, common_location):
	min_box = ' '.join(min_box)
	max_box = ' '.join(max_box)

	with open('lib/tcl/solvate.tcl','r') as solvate_tcl:
		with open('lib/tcl/solvate.tmp.tcl','w') as solvate_tcl_tmp:
			for line in solvate_tcl:
				solvate_tcl_tmp.write(line.replace('min_size_water_box', min_box).replace('max_size_water_box', max_box))

	command = 'vmd -dispdev text -e %s/lib/tcl/solvate.tmp.tcl' % (location)
	util.call_subprocess(command, common_location, True)

	os.remove('lib/tcl/solvate.tmp.tcl')

def ionize(ions_concetration, location, common_location):
	command = "env concentration='%s' vmd -dispdev text -e %s/lib/tcl/ionize.tcl" % (ions_concetration, location)
	
	util.call_subprocess(command, common_location, True)
	shutil.copy2(common_location+'/ionized.psf', common_location+'/system.psf')
	shutil.copy2(common_location+'/ionized.pdb', common_location+'/system.pdb')