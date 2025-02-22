SIM = modelsim

# Define the top-level language
TOPLEVEL_LANG = verilog

# Path to all Verilog source files (wildcard to include all .v files in the directory)
VERILOG_SOURCES += $(wildcard ../SuperScalar/*.v)


TOPLEVEL = processor
# The Python file containing Cocotb testbenches
MODULE = test_processor


export WAVES=1

# Simulation arguments
SIM_ARGS += -voptargs=+acc
SIM_ARGS += -L work
SIM_ARGS += -L lpm_ver
SIM_ARGS += -L altera_mf_ver


include $(shell cocotb-config --makefiles)/Makefile.sim

