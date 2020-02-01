@echo off

@echo Making sure PIP is up to date
python -m pip install --upgrade pip
@echo.

@echo Verifying PIP dependencies
pip install pillow
@echo.

@echo Making sure TABLE is up to date
git pull
@echo.

pause