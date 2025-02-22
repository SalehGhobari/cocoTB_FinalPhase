onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -radix unsigned /testbench/clk
add wave -noupdate -radix unsigned /testbench/rst
add wave -noupdate -radix unsigned /testbench/enable
add wave -noupdate -radix unsigned /testbench/PC
add wave -noupdate -radix hexadecimal /testbench/uut/instMem/q_a
add wave -noupdate -radix hexadecimal /testbench/uut/instMem/q_b
add wave -noupdate -radix unsigned /testbench/uut/writeRegister1W
add wave -noupdate -radix unsigned /testbench/uut/writeData1
add wave -noupdate -radix unsigned /testbench/uut/writeRegister2W
add wave -noupdate -radix unsigned /testbench/uut/writeData2
add wave -noupdate -radix unsigned /testbench/uut/CorrectedPC1
add wave -noupdate -radix unsigned /testbench/uut/CorrectedPC2
add wave -noupdate -radix unsigned /testbench/uut/instMemMuxOut
add wave -noupdate -radix unsigned /testbench/uut/instMemPred
add wave -noupdate -radix unsigned /testbench/uut/instMemTarget
add wave -noupdate -radix unsigned /testbench/uut/prediction1
add wave -noupdate -radix unsigned /testbench/uut/prediction2
add wave -noupdate -radix unsigned /testbench/uut/BJPC
add wave -noupdate -radix unsigned /testbench/uut/nextPC
add wave -noupdate -radix unsigned /testbench/uut/CPC
add wave -noupdate /testbench/uut/branch_taken1
add wave -noupdate /testbench/uut/branch_taken2
add wave -noupdate -radix decimal /testbench/uut/ForwardBranchA
add wave -noupdate -radix decimal /testbench/uut/ForwardBranchB
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {207844 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 215
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
WaveRestoreZoom {166996 ps} {267311 ps}
