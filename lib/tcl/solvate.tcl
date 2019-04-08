package require solvate
solvate system.psf system.pdb -o solvate -b 1.5 -minmax {{min_size_water_box} {max_size_water_box}}
exit
