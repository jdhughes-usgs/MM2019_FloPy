@echo off
call :normalizepath %cd%\..\Miniconda3
set mc3=%retval%
echo Miniconda installed in %mc3%


rem install python packages
%mc3%\python install_packages.py


rem pause so screen will not go away
pause


:: ========== FUNCTIONS ==========
exit /B

:normalizepath
  set retval=%~dpfn1
  exit /B
