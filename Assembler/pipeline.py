import subprocess
import os
import sys
from pathlib import Path

def run_scheduler(scheduler_path, output_file):
    """
    Run the Python scheduler script
    """
    try:
        result = subprocess.run([sys.executable, scheduler_path],
                              cwd=scheduler_path.parent,
                              check=True,
                              capture_output=True,
                              text=True)
        print("Scheduler completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running scheduler: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def compile_and_run_assembler(assembler_java, input_file):
    """
    Compile and run the Java assembler
    """
    assembler_dir = assembler_java.parent
    
    # First compile the Java file
    try:
        compile_result = subprocess.run(['javac', assembler_java.name],
                                      cwd=assembler_dir,
                                      check=True,
                                      capture_output=True,
                                      text=True)
        print("Java compilation completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Java file: {e}")
        print(f"Compilation error output: {e.stderr}")
        sys.exit(1)

    # Then run the compiled class file
    try:
        # Get the class name without .java extension
        class_name = assembler_java.stem
        # Run the compiled Java class
        run_result = subprocess.run(['java', class_name, input_file],
                                  cwd=assembler_dir,
                                  check=True,
                                  capture_output=True,
                                  text=True)
        print("Assembler completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running assembler: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def run_loadmif(loadmif_path):
    """
    Run the Python loadmif script
    """
    try:
        result = subprocess.run([sys.executable, loadmif_path.name],
                              cwd=loadmif_path.parent,
                              check=True,
                              capture_output=True,
                              text=True)
        print("LoadMIF completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running loadmif script: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    # Get the current directory
    current_dir = Path(__file__).parent

    # Configuration - paths relative to current directory
    SCHEDULER_PATH = current_dir / "scheduler.py"
    ASSEMBLER_JAVA = current_dir / "Assembler.java"
    LOADMIF_PATH = current_dir / "loadMif.py"
    SCHEDULED_INSTRUCTIONS = current_dir / "scheduled_instructions.txt"

    # Validate file paths
    for path in [SCHEDULER_PATH, ASSEMBLER_JAVA, LOADMIF_PATH]:
        if not path.exists():
            print(f"Error: {path} does not exist")
            sys.exit(1)

    print("Starting automated build process...")

    # Run each step in sequence
    print("\n1. Running scheduler...")
    run_scheduler(SCHEDULER_PATH, SCHEDULED_INSTRUCTIONS)

    print("\n2. Compiling and running assembler...")
    compile_and_run_assembler(ASSEMBLER_JAVA, SCHEDULED_INSTRUCTIONS)

    print("\n3. Running loadmif script...")
    run_loadmif(LOADMIF_PATH)

    print("\nBuild process completed successfully!")

if __name__ == "__main__":
    main()