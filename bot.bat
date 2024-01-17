@echo off
set VENV_PATH=venv
set MAIN_SCRIPT=main.py 

echo Activating the virtual environment...
call %VENV_PATH%\Scripts\activate

echo Running the Python script...
python %MAIN_SCRIPT%

echo complete
