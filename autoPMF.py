import sys
import subprocess
import configparser
import shutil
import pprint
import os
from lib.py import util, build

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
		build.splitChains(stand_files['PDB file'], init_config['ligand selection'], init_config['protein selection'], sys_inf['location'], common_location)

		#GENERATING PDB AND PSF
		build.generatePSF(stand_files['parameters'], 'system', sys_inf['location'], common_location)

		#USING MUSTANG
		build.splitChains('base.pdb', 'chain A', 'chain B', sys_inf['location'], common_location)

		build.generatePSF(stand_files['parameters'], 'base-complex', sys_inf['location'], common_location)

		command = '../lib/thirty/mustang/bin/mustang-3.2.3 -p ./ -i base-complex.pdb system.pdb -o aligned -r ON'
		util.call_subprocess(command, common_location, True)

		# build.splitChains('system.pdb', 'chain A', 'chain B', sys_inf['location'],common_location)

		# build.generatePSF(stand_files['parameters'], 'system', sys_inf['location'], common_location)

		# #SOLVATING
		# build.solvate(init_config['minimum size of water box'], init_config['maximum size of water box'].split(','), sys_inf['location'], common_location)

		# #IONAZING
		# build.ionize(init_config['ions concentratrion'], sys_inf['location'], common_location)

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