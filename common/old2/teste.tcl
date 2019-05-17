# package require Orient
# namespace import Orient::orient

# set sel [atomselect top "chain A or chain B"]
# set I [draw principalaxes $sel]
# # set A [orient $sel [lindex $I 2] {0 0 1}]
# # $sel move $A
# # set I [draw principalaxes $sel]
# # set A [orient $sel [lindex $I 1] {0 1 0}]
# # $sel move $A
# # set I [draw principalaxes $sel]
# set all [atomselect top "chain A or chain B"]

# # set angle 0.001
# # set x [lindex [measure center [atomselect top "chain B"] weight mass] 0]

# # while {abs($x) > 0.001 & $angle<360} { 
# # 	$all move [transaxis z $angle]
# #     set angle [expr $angle + 0.001]
# # 	set x [lindex [measure center [atomselect top "chain B"] weight mass] 0]
# # }

# set angle 0.001
# set y [lindex [measure center [atomselect top "chain B"] weight mass] 1]
# set z [lindex [measure center [atomselect top "chain B"] weight mass] 2]
# set true 1
# while {$true == 1} { 
# 	$all move [transaxis x $angle]
#     set angle [expr $angle + 0.001]
# 	set y [lindex [measure center [atomselect top "chain B"] weight mass] 1]
# 	set z [lindex [measure center [atomselect top "chain B"] weight mass] 2]
# 	if {abs($y) < 0.001 & abs($z) == $z} {
# 		set true 0
# 	}
# }
set teste "chain A"
set teste2 "chain B"
set x [concat $teste " or " $teste2]
puts $x