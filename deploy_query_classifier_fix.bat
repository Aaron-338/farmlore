@echo off
REM Deploy query classifier fix to Docker container

REM Set variables
set CONTAINER_NAME=farmlore-web-1
set PATCH_FILE=docker_fix_query_classifier.py
set CONTAINER_PATH=/app/

echo Deploying query classifier fix to Docker container...

REM Check if the container is running
docker ps | findstr %CONTAINER_NAME% >nul 2>&1
if errorlevel 1 (
  echo Error: Container %CONTAINER_NAME% is not running.
  echo Please make sure the container is running before deploying the fix.
  exit /b 1
)

REM Copy the patch file to the container
echo Copying patch script to container...
docker cp %PATCH_FILE% %CONTAINER_NAME%:%CONTAINER_PATH%

REM Execute the patch script in the container
echo Executing the patch script in the container...
docker exec %CONTAINER_NAME% python /app/docker_fix_query_classifier.py

REM Check if the script executed successfully
if errorlevel 1 (
  echo Error: Failed to apply the patch.
  echo Check the container logs for more details.
  exit /b 1
) else (
  echo Patch applied successfully!
  echo The query classifier has been fixed.
  echo.
  echo You can now test with queries like:
  echo - "What are natural predators for aphids?"
  echo - "What beneficial insects eat aphids?"
  echo These will now be correctly classified as pest management queries.
)

REM Optional: Display web service logs
echo.
echo Displaying web service logs to confirm patch (press Ctrl+C to stop)...
docker logs -f %CONTAINER_NAME% 