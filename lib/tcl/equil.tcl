mol load psf ../common/aligned.psf pdb ../common/aligned.pdb
set all [atomselect top all]
$all set occupancy 0
$all set beta 0
$all writepdb refumb0.pdb

set all [atomselect top all]
$all set occupancy 0
$all set beta 0
set pr [atomselect top "chain A and backbone"]
$pr set occupancy 1.0
$all writepdb atoms.pdb

exit
