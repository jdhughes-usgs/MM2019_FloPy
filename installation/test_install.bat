@echo off
call :normalizepath %cd%\..\Miniconda3
set mc3=%retval%


rem test python packages
%mc3%\python test_root_install.py


rem pause so screen will not go away
pause


:: ========== FUNCTIONS ==========
exit /B

:normalizepath
  set retval=%~dpfn1
  exit /B
