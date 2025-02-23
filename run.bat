@echo off
:: Change to the script's directory
cd /d "%~dp0"

:: Activate virtual environment
cd /d "%~dp0cocoTB_venv\Scripts"
call activate.bat

cd /d "../"

:: Run pipeline.py in Assembler directory
cd /d "%~dp0Assembler"
python pipeline.py
if errorlevel 1 (
    echo Error running pipeline.py
    pause
    exit /b 1
)

:: Run make clean and make in testbenches directory
cd /d "%~dp0testbenches"
"%PROGRAMFILES%\Git\bin\sh.exe" --login -c "make clean && make > ../verification/coco_out.txt"
if errorlevel 1 (
    echo Error running make commands
    pause
    exit /b 1
)

:: Run main.py in Cycle Accurate Simulator directory
cd /d "%~dp0Cycle Accurate Simulator"
python main.py > ../verification/cas_out.txt
if errorlevel 1 (
    echo Error running main.py
    pause
    exit /b 1
)

:: Run verify.py in Verification directory
cd /d "%~dp0Verification"
python verify.py
if errorlevel 1 (
    echo Error running verify.py
    pause
    exit /b 1
)

echo Pipeline completed successfully
pause