@echo off
REM Deploy prompt template fix to Docker container

REM Set variables
set CONTAINER_NAME=farmlore-web-1
set SCRIPT_FILE=fix_prompt_templates.py
set CONTAINER_PATH=/app/

echo Deploying prompt template fix to Docker container...

REM Check if the container is running
docker ps | findstr %CONTAINER_NAME% >nul 2>&1
if errorlevel 1 (
  echo Error: Container %CONTAINER_NAME% is not running.
  echo Please make sure the container is running before deploying the fix.
  exit /b 1
)

REM Wait for the container to be fully started
echo Waiting for container to be fully started (5 seconds)...
timeout /t 5 /nobreak

REM Copy the script to the container
echo Copying prompt template fix script to container...
docker cp %SCRIPT_FILE% %CONTAINER_NAME%:%CONTAINER_PATH%

REM Execute the script in the container
echo Executing the prompt template fix script in the container...
docker exec %CONTAINER_NAME% python /app/fix_prompt_templates.py

REM Check if the script executed successfully
if errorlevel 1 (
  echo Error: The prompt template fix script failed to execute successfully.
  exit /b 1
)

REM Restart the container to ensure changes take effect
echo Restarting the container to ensure changes take effect...
docker restart %CONTAINER_NAME%

echo Waiting for container to restart (15 seconds)...
timeout /t 15 /nobreak

echo.
echo =========================================================
echo Prompt template fix deployment complete! Container has been restarted.
echo.
echo To test the fix, try sending the query:
echo   - "What are natural predators for aphids?"
echo.
echo You should now see it correctly classified as pest_management
echo and responding with appropriate pest management information.
echo ========================================================= 