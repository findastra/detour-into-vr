@echo off
rem Starts the Detour Twitch recorder in its own window. Safe to run again after a reboot.
del "%USERPROFILE%\Videos\detour-into-vr\twitch-recordings\STOP" 2>nul
python "%~dp0record_detour.py" --until "2026-10-11 05:00"
