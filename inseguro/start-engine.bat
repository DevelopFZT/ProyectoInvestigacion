@echo off
start cmd /k "python server.py"
timeout /t 5
start cmd /k "python client.py"