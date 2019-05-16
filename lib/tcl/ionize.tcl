package require autoionize
autoionize -psf solvate.psf -pdb solvate.pdb -sc $env(concentration)
exit
