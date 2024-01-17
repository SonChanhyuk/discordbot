@echo off
echo Creating and activating a virtual environment...
python -m venv venv

echo Activating the virtual environment...
call venv\Scripts\activate

echo Installing packages from requirements.txt...
pip install -r requirements.txt

echo Virtual environment and packages installation complete.

