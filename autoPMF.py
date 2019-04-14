import sys
import subprocess
import configparser
import shutil
import pprint
import os
from lib.py import util

config = configparser.ConfigParser(inline_comment_prefixes=';')
config.read('input.in')

goFoward=True
stage=""

try:
	stage=str(sys.argv[1])
except:
	print('ERROR: It\'s necessary to inform the stage of the analysis.')
	goFoward=False

if (goFoward):
	sys_inf = config['system.information']

	if (stage == 'init'):
		current_dir = os.getcwd()
		if (current_dir == sys_inf['location']):
			util.createDir(sys_inf['location']+'/common')
		else:
			print("Directory location informathe does not match with the current directory. Please, verify")

	if (stage == 'build'):

		init_config = config['build.system']
		sys_inf = config['system.information']
		stand_files = config['standard.files']
		common_location = sys_inf['location']+"/common"

		#SPLITING CHAINS
		command = "env pdb_file='%s' protein_selection='%s' ligand_selection='%s' vmd -dispdev text -e %s/lib/tcl/split.tcl" % (stand_files['PDB file'], init_config['ligand selection'], init_config['protein selection'], sys_inf['location'])
		util.call_subprocess(command, common_location, True)

		#GENERATING PSF E PDB FILE
		parameters = stand_files['parameters'].split(',')

		psf_tcl = open('lib/tcl/psf.tcl','r').readlines()

		for x in range(0, len(parameters)):
			psf_tcl.insert(x+1,'topology '+parameters[x].strip()+"\n")

		# aliases = open(common_location+'/alias.in').readlines()
		# for y in range(0, len(aliases)):
		# 	psf_tcl.insert(y+4, aliases[y])#x+5->second line

		psf_tcl_tmp = open('lib/tcl/psf.tmp.tcl','w')
		psf_tcl = ''.join(psf_tcl)
		psf_tcl_tmp.write(psf_tcl)
		psf_tcl_tmp.close()

		command = 'vmd -dispdev text -e '+sys_inf['location']+'/lib/tcl/psf.tmp.tcl'
		util.call_subprocess(command, common_location, True)

		os.remove('lib/tcl/psf.tmp.tcl')

		#SOLVATING
		min_box = ' '.join(init_config['minimum size of water box'].split(','))
		max_box = ' '.join(init_config['maximum size of water box'].split(','))

		with open('lib/tcl/solvate.tcl','r') as solvate_tcl:
			with open('lib/tcl/solvate.tmp.tcl','w') as solvate_tcl_tmp:
				for line in solvate_tcl:
					solvate_tcl_tmp.write(line.replace('min_size_water_box', min_box).replace('max_size_water_box', max_box))

		command = 'vmd -dispdev text -e '+sys_inf['location']+'/lib/tcl/solvate.tmp.tcl'
		util.call_subprocess(command, common_location, True)

		os.remove('lib/tcl/solvate.tmp.tcl')

		#IONAZING
		command = 'vmd -dispdev text -e '+sys_inf['location']+'/lib/tcl/ionize.tcl'
		util.call_subprocess(command, common_location, True)

		shutil.copy2(common_location+'/ionized.psf', common_location+'/system.psf')
		shutil.copy2(common_location+'/ionized.pdb', common_location+'/system.pdb')

	if (stage == 'equil'):
		util.createDir(sys_inf['location']+'/equil')
		
		equilibration = config['build.system']
		sys_inf = config['system.information']

		#util.copyAllFilesWith(+sys_inf['location']'/lib/base-files', sys_inf['location']+'equil/', '*eq*')

		#Mount the system
		util.call_subprocess('vmd -dispdev text -e '+sys_inf['location']+'/lib/tcl/equil.tcl', sys_inf['location']+'equil/', True)

		util.editConfigFile(sys_inf['location']+'/lib/base-files/conf_eq')
		
		#Update the dummy atom
		util.update_dummy(sys_inf['location']+'/equil', ['colv-equil'], 'common/system.pdb', 'chain A and backbone', stage)

	# if (stage == 'smd')