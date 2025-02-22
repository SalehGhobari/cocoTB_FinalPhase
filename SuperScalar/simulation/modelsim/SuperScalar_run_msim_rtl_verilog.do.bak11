transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/BranchPredictionUnit.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/muxes.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/processor.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/registerFile.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/controlUnit.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/ALU.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/signextender.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/programCounter.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/adder.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/ANDGate.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/XNOR.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/Pipes.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/Comparator.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/forwardingUnit.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/HazardDetectionUnit.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/ORGate.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/pcCorrection.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/dual_issue_data_memory.v}
vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/dual_issue_inst_mem.v}

vlog -vlog01compat -work work +incdir+C:/Users/Ahmad/Desktop/github/JoSDC/Innovation\ Phase/SuperScalar {C:/Users/Ahmad/Desktop/github/JoSDC/Innovation Phase/SuperScalar/testbench.v}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L fiftyfivenm_ver -L rtl_work -L work -voptargs="+acc"  testbench

add wave *
view structure
view signals
run -all
