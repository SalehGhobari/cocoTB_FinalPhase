# The Plumbers Team - Cocotb Verification

This repository contains the Cocotb-based verification framework for a Verilog HDL design, developed for the JoSDC 2024 competition. The goal is to validate a dual-issue superscalar processor using simple testbenches.

## Prerequisites

### Required Software

Ensure the following software is installed and properly configured:

- **Quartus Prime Lite (Free Version)**
  - Make sure ModelSim (32-bit, bundled with Quartus Prime Lite) is installed and set in the system `PATH` variable.
- **Python (32-bit version, 3.13.2 recommended as of writing this README)**
  - A 32-bit Python version is required to avoid DLL architecture mismatches with ModelSim.
  - While it is possible to switch to Questa or another simulator, using a 32-bit Python version was the easiest integration approach in this setup.
- **Git**
  - Windows: Install via [Git for Windows](https://git-scm.com/download/win)
  - Linux: Install using package manager (`sudo apt install git` or equivalent)
- **Make**
  - Windows: Install via [Chocolatey](https://chocolatey.org/install)
    ```sh
    choco install make
    ```
  - Linux: Already included in most distributions.

## Setup Instructions

### Clone the Repository

```sh
git clone https://github.com/SalehGhobari/cocoTB.git
cd cocoTB
```

### Create a Virtual Environment

Inside the cloned repository directory:

```sh
python -m venv cocoTB_venv
```

### Activate Virtual Environment

- **Windows:**
  ```sh
  cocoTB_venv\Scripts\activate.bat
  ```
- **Linux/macOS:**
  ```sh
  source cocoTB_venv/bin/activate
  ```

### Install Dependencies

```sh
pip install cocotb cocotb-test
```

## Running Tests

### Makefile

The project uses a Makefile to run tests with ModelSim.

```make
SIM = modelsim

# Define the top-level language
TOPLEVEL_LANG = verilog

# Path to all Verilog source files (includes all .v files in the directory)
VERILOG_SOURCES += $(wildcard ../SuperScalar/*.v)

TOPLEVEL = processor
MODULE = test_processor

export WAVES=1

# Simulation arguments
SIM_ARGS += -voptargs=+acc
SIM_ARGS += -L work
SIM_ARGS += -L lpm_ver
SIM_ARGS += -L altera_mf_ver

include $(shell cocotb-config --makefiles)/Makefile.sim
```

- Modify `MODULE` and `TOPLEVEL` to match the module you want to test.
- Place the `.mif` files required for any IP modules used in the top-level design inside the `testbenches` directory where the Makefile is located.
- Testbenches of the individual components contain randomized input sets for functional verification but the top level design was tested using the benchmarks given by the committee.
- Refer to the [Cocotb documentation](https://docs.cocotb.org/) for further details on using Makefiles.

### Running Tests

1. **Run the provided script**:

   - On Windows, execute `run.bat` from the repository root:
     ```sh
     run.bat
     ```
     **Note:** This script only works on Windows and requires the user to be logged into Git with it installed.

2. **Navigate to testbenches directory**:

   ```sh
   cd cocoTB/testbenches
   ```

3. **Clean previous builds**:

   ```sh
   make clean
   ```

4. **Run the testbench**:

   ```sh
   make
   ```


# JoSDC-2024-Verification-cocoTB-
modules tested : ORGate4 ✅ ORGate ✅ adder ✅ ANDGate ✅ ANDGate3 ✅ Comparator ✅ programCounter ✅ ALU ✅ controlUnit ✅ Pipes ✅ XNOR ✅ mux2x1 ✅ mux3to1 ✅ mux3to1 ✅ mux5to1 ✅ signextender ✅ registerFile ✅  mux2x1En ✅ HazardDetectionUnit ✅ forwardingUnit ✅ pcCorrection ✅ BranchPredictionUnit ✅
