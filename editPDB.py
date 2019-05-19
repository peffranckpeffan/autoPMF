import numpy as np

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
					final_pdb.write(new_pdb_lines[i])
				else:
					final_pdb.write(new_pdb_lines[i].replace(' B ', ' A '))


		