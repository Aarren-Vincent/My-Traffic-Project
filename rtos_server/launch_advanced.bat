@echo off
title Advanced RTOS Traffic Control System
echo ================================================
echo   ADVANCED RTOS TRAFFIC CONTROL SYSTEM
echo ================================================
echo.
echo This system includes:
echo • Real-time performance metrics
echo • Data logging to CSV
echo • Weather simulation
echo • Adaptive traffic control
echo • Virtual sensor simulation
echo • Deadline monitoring
echo.
echo ================================================
echo.

echo [1] Starting Advanced RTOS Server...
start "ADVANCED RTOS SERVER" cmd /k "cd /d D:\project\MyTrafficProject\rtos_server && python rtos_server_advanced.py"
timeout /t 5 /nobreak >nul

echo [2] Starting Advanced Visualization...
start "ADVANCED VISUALIZATION" cmd /k "cd /d D:\project\MyTrafficProject\python_simulator && python traffic_simulator_advanced.py"

echo.
echo ================================================
echo   SYSTEM STARTED SUCCESSFULLY!
echo ================================================
echo.
echo FEATURES DEMONSTRATED:
echo • Real-time task scheduling (RTOS Core Concept)
echo • Priority-based preemption (Emergency vs Normal)
echo • Hard deadline monitoring (500ms response)
echo • Performance metrics collection
echo • Adaptive control (Weather/traffic effects)
echo • Data logging for analysis
echo.
echo CONTROLS in Visualization:
echo   E = Trigger Emergency Vehicle
echo   P = Pedestrian Crossing (Shift+P for EW)
echo   W = Cycle Weather
echo   R = Reset Metrics
echo   G = Generate Report
echo   ESC = Quit
echo.
echo Check the RTOS window for real-time metrics!
echo Data is logged to: traffic_log.csv
echo ================================================
echo.
echo Press any key to close this launcher...
pause >nul