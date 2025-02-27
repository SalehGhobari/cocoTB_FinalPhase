import subprocess
from pathlib import Path

# Get the base project directory (assuming we're in the Innovation Phase folder)
project_root = Path(__file__).parent.parent  # Goes up one level from current script

# Define paths relative to project root
assembler_dir = project_root / "Assembler"
java_file = "Assembler"
output_mif = project_root / "SuperScalar" / "dual_issue_inst_memory.mif"
output_mif_cocotb = project_root / "testbenches" / "dual_issue_inst_memory.mif"

# Ensure directories exist
assembler_dir.mkdir(parents=True, exist_ok=True)
output_mif.parent.mkdir(parents=True, exist_ok=True)
output_mif_cocotb.parent.mkdir(parents=True, exist_ok=True)

# Compile Java file
subprocess.run(
    ["javac", f"{java_file}.java"],
    cwd=assembler_dir,
    check=True
)

# Run Java program and write output to MIF file
with open(output_mif, "w") as mif_file:
    subprocess.run(
        ["java", java_file],
        cwd=assembler_dir,
        stdout=mif_file,
        text=True,
        check=True
    )

with open(output_mif_cocotb, "w") as mif_file:
    subprocess.run(
        ["java", java_file],
        cwd=assembler_dir,
        stdout=mif_file,
        text=True,
        check=True
    )

print(f"Assembly complete. The .mif file has been updated at: {output_mif}")