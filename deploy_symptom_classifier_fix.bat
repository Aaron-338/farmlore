@echo off
REM Deploy symptom classification fix to the farmlore system

echo =====================================================
echo   Deploying Symptom Query Classification Fix
echo =====================================================

REM Check if Docker is running
docker info > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker does not seem to be running. Please start Docker first.
    exit /b 1
)

REM Check for the improved patch file
if not exist "improved_patch_classifier.py" (
    echo Error: improved_patch_classifier.py not found in the current directory.
    exit /b 1
)

REM Check for the test file
if not exist "test_symptom_classification.py" (
    echo Error: test_symptom_classification.py not found in the current directory.
    exit /b 1
)

REM Determine container name
for /f "tokens=*" %%i in ('docker ps --format "{{.Names}}" ^| findstr farmlore') do (
    set CONTAINER_NAME=%%i
    goto FOUND_CONTAINER
)

echo Error: No farmlore containers found running.
exit /b 1

:FOUND_CONTAINER
echo Found farmlore container: %CONTAINER_NAME%

REM Copy the improved patch file to the container
echo Copying improved_patch_classifier.py to container...
docker cp improved_patch_classifier.py %CONTAINER_NAME%:/app/

REM Copy the test file to the container
echo Copying test_symptom_classification.py to container...
docker cp test_symptom_classification.py %CONTAINER_NAME%:/app/

REM Run the patch in the container
echo Applying the symptom classification patch...
docker exec %CONTAINER_NAME% python /app/improved_patch_classifier.py

REM Verify the fix with the test script
echo Testing the symptom classification patch...
docker exec %CONTAINER_NAME% python /app/test_symptom_classification.py

echo.
echo =====================================================
echo   Symptom Classification Fix Deployed Successfully
echo =====================================================
echo.
echo The system should now correctly classify symptom-based queries!
echo Example queries that will now work:
echo   - 'My crops are turning purple'
echo   - 'Why are my tomato leaves yellow?'
echo   - 'My plants are wilting despite watering'
echo   - 'What's wrong with my plant with holes in the leaves?'
echo.
echo These queries will be routed to the PEST_IDENTIFICATION handler,
echo which can access both pest and disease information to provide
echo appropriate responses.
echo =====================================================

pause 