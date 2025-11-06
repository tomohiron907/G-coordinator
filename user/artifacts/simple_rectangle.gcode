; Basic start sequence for tutorial rectangle print
G90 ; absolute positioning
G21 ; metric units
G28 ; home all axes
M82 ; absolute extrusion
G92 E0 ; reset extruder

M140 S60 
M190 S60 
M104 S205 
M109 S205 
M106 S255 
M83 ;relative extrusion mode 
G1 F3600 X0.0 Y0.0 Z0.0
G1 F1800 X10.00000 Y0.00000 Z0.00000 E0.33260
G1 F1800 X10.00000 Y10.00000 Z0.00000 E0.33260
G1 F1800 X0.00000 Y10.00000 Z0.00000 E0.33260
G1 F1800 X0.00000 Y0.00000 Z0.00000 E0.33260
; Basic end sequence for tutorial rectangle print
M400
M104 S0
M140 S0
G91
G1 Z5 F1800
G90
G1 X0 Y0 F3000
M82
G92 E0
M84
