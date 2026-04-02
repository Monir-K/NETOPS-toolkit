@echo off
REM NetOps Toolkit Launcher — By M Kamjo
REM Opens in InPrivate mode so no history/cookies saved

REM Try Edge InPrivate first
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --inprivate --start-fullscreen "http://localhost:5199"

REM If Edge not found, try Chrome Incognito (fallback):
REM start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --incognito --start-fullscreen "http://localhost:5199"
