@echo off
REM Deploy improved patch for query classifier fix to Docker container

REM Set variables
set CONTAINER_NAME=farmlore-web-1
set PATCH_FILE=improved_patch_classifier.py
set CONTAINER_PATH=/app/

echo Deploying improved query classifier fix to Docker container...

REM Check if the container is running
docker ps | findstr %CONTAINER_NAME% >nul 2>&1
if errorlevel 1 (
  echo Error: Container %CONTAINER_NAME% is not running.
  echo Please make sure the container is running before deploying the fix.
  exit /b 1
)

REM Copy the patch file to the container
echo Copying improved patch script to container...
docker cp %PATCH_FILE% %CONTAINER_NAME%:%CONTAINER_PATH%

REM Execute the patch script in the container
echo Executing the improved patch script in the container...
docker exec %CONTAINER_NAME% python /app/improved_patch_classifier.py

REM Check if the script executed successfully
if errorlevel 1 (
  echo Error: The patch script failed to execute successfully.
  exit /b 1
)

REM Restart the container to ensure changes take effect
echo Restarting the container to ensure changes take effect...
docker restart %CONTAINER_NAME%

echo Waiting for container to restart (15 seconds)...
timeout /t 15 /nobreak

echo.
echo =========================================================
echo Patch deployment complete! Container has been restarted.
echo.
echo To test the fix, try sending the following queries:
echo   - "How do I control aphids on roses?"
echo   - "What are natural predators for aphids?"
echo.
echo Both should now be classified as pest_management queries.
echo ========================================================= 