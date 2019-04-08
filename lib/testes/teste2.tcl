set inZ 0
set comMdm2 [measure center [atomselect top "chain B"] weight mass]
set z [lindex [lindex $I 2] 2]
set zAxe [lindex $I 2]
while {$inZ == 0} {
	set angle  [expr acos([vecdot $comMdm2 $zAxe]/ [vecdot $comMdm2 $comMdm2]* [vecdot $zAxe $zAxe])]
	puts $angle
	#$all move [transaxis x $angulo]
    #set $zAxe [list [lindex $I 0] [lindex $I 1] [expr [lindex $I 2] + 0.1]]
    if {$z>3} {
    	set $inZ 1 
    }
}