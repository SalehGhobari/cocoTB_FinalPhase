onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /processor/clk
add wave -noupdate /processor/enable
add wave -noupdate /processor/rst
add wave -noupdate -radix unsigned /processor/PC
add wave -noupdate -radix hexadecimal /processor/instMem/q_a
add wave -noupdate -radix hexadecimal /processor/instMem/q_b
add wave -noupdate -radix decimal /processor/writeRegister1W
add wave -noupdate -radix unsigned /processor/writeData1
add wave -noupdate -radix decimal /processor/writeRegister2W
add wave -noupdate -radix unsigned /processor/writeData2
add wave -noupdate -radix unsigned /processor/CorrectedPC1
add wave -noupdate -radix unsigned /processor/CorrectedPC2
add wave -noupdate -radix unsigned /processor/instMemMuxOut
add wave -noupdate /processor/instMemPred
add wave -noupdate -radix decimal /processor/instMemTarget
add wave -noupdate /processor/prediction1
add wave -noupdate /processor/prediction2
add wave -noupdate -radix unsigned /processor/BJPC
add wave -noupdate -radix unsigned /processor/nextPC
add wave -noupdate -radix unsigned /processor/CPC
add wave -noupdate /processor/branch_taken1
add wave -noupdate /processor/branch_taken2
add wave -noupdate /processor/ForwardBranchA
add wave -noupdate /processor/ForwardBranchB
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {207844 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 190
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {217713 ps}
