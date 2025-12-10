(==== DrawMate Calibration Pattern ====)
(Measure these distances to calibrate $100 and $101)

G21         ; millimeters
G90         ; absolute positioning
F1500       ; feed rate

G0 Z10      ; pen up

; X AXIS CALIBRATION LINE
G0 X0 Y0
G0 Z0       ; pen down
G1 X100 Y0
G0 Z10      ; pen up

; Y AXIS CALIBRATION LINE
G0 X0 Y0
G0 Z0       ; pen down
G1 X0 Y100
G0 Z10

; 100x100 CALIBRATION SQUARE
G0 X0 Y0
G0 Z0       ; pen down
G1 X100 Y0
G1 X100 Y100
G1 X0 Y100
G1 X0 Y0
G0 Z10

G0 X0 Y0
M2