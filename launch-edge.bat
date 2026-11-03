@echo off
REM NetOps Toolkit Launcher — By M Kamjo
REM Uses a regular browser profile so local accounts and data persist

REM Try Edge first
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --start-fullscreen "http://localhost:5199"

REM If Edge is not installed, open Chrome:
REM start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --start-fullscreen "http://localhost:5199"
