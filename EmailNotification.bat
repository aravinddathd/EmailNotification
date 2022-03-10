@echo off
set /P Github="Enter Github Link"
echo %Github%
set /P Folder="Enter Repository Folder name"
echo %Folder%
git clone %Github%
%cd%\cloc-1.64.exe %cd%\%Folder% > Input.txt

python C:\Users\Aravind\Desktop\Checkmarx\EmailNotification.py 