mol load pdb ../../../mdm2-p53/common/1ycr.pdb
set all [atomselect top all]
$all moveby [vecinvert [measure center $all weight mass]]

package require Orient
namespace import Orient::orient

set sel [atomselect top "all"]
set I [draw principalaxes $sel]
set A [orient $sel [lindex $I 2] {0 0 1}]
$sel move $A
set I [draw principalaxes $sel]
set A [orient $sel [lindex $I 1] {0 1 0}]
$sel move $A
set I [draw principalaxes $sel]
#$sel move [transaxis z 23.2879423356]
# set sel2 [atomselect top "resid 88 to 954"]
# set I2 [draw principalaxes $sel2]
# puts $I2

# set comMdm2 [measure center [atomselect top "chain B"] weight mass]
# set z [lindex [lindex $I 2] 2]
# set zAxe [lindex $I 2]
# set angle  [expr acos([vecdot $comMdm2 $zAxe]/ [vecdot $comMdm2 $comMdm2]* [vecdot $zAxe $zAxe])]
# puts [expr $angle * 180 / 3.1415926535897931]
# set sel [atomselect top "all"]
# $sel move [transaxis z [expr $angle * 180 / 3.1415926535897931]]
# graphics top sphere [measure center [atomselect top "chain B"] weight mass]

# set sel2 [atomselect top "chain B"]
# set I2 [draw principalaxes $sel2]
# set A [orient $sel [lindex $I2 2] [lindex $I 2]]
# $sel move $A
# set I2 [draw principalaxes $sel2]
# set A [orient $sel [lindex $I2 1] [lindex $I 1]]
# $sel move $A

# set a [atomselect top $env(protein_selection)]
# $a writepdb prot.pdb
# set b [atomselect top $env(ligand_selection)]
# $b writepdb lig.pdb
# exit