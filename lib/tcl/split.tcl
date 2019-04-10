mol load pdb $env(pdb_file)

set x [join [concat $env(protein_selection) " or "] "" ]
set all [atomselect top [join [concat $x $env(ligand_selection)] "" ]]
$all moveby [vecinv [measure center $all weight mass]]

package require Orient
namespace import Orient::orient

set sel [atomselect top [join [concat $x $env(ligand_selection)] "" ]]
set I [draw principalaxes $sel]
set A [orient $sel [lindex $I 2] {0 0 1}]
$sel move $A
set I [draw principalaxes $sel]
set A [orient $sel [lindex $I 1] {0 1 0}]
$sel move $A
set I [draw principalaxes $sel]

set angle 0.001
set x [lindex [measure center [atomselect top $env(ligand_selection)] weight mass] 0]

while {abs($x) > 0.001 & $angle<360} { 
	$all move [transaxis z $angle]
    set angle [expr $angle + 0.001]
	set x [lindex [measure center [atomselect top $env(ligand_selection)] weight mass] 0]
}

set angle 0.001
set y [lindex [measure center [atomselect top $env(ligand_selection)] weight mass] 1]
set z [lindex [measure center [atomselect top $env(ligand_selection)] weight mass] 2]
set true 1
while {$true == 1} { 
	$all move [transaxis x $angle]
    set angle [expr $angle + 0.001]
	set y [lindex [measure center [atomselect top $env(ligand_selection)] weight mass] 1]
	set z [lindex [measure center [atomselect top $env(ligand_selection)] weight mass] 2]
	if {abs($y) < 0.001 & abs($z) == $z} {
		set true 0
	}
}

set a [atomselect top $env(protein_selection)]
$a writepdb prot.pdb
set b [atomselect top $env(ligand_selection)]
$b writepdb lig.pdb
exit