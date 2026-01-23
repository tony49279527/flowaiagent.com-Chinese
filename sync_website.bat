@echo off
echo Starting Website Sync...
echo --------------------------------
echo 1. Adding files...
"C:\Program Files\Git\bin\git.exe" add .

echo 2. Committing changes...
set /p commit_msg="Enter commit message (Press Enter for 'Update website'): "
if "%commit_msg%"=="" set commit_msg=Update website
"C:\Program Files\Git\bin\git.exe" commit -m "%commit_msg%"

echo 3. Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

echo --------------------------------
echo Sync Complete!
pause
