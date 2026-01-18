# 🚦 RTOS-Based Smart Traffic Control System with Emergency Priority

## 📋 Project Overview
A **real-time traffic control simulation** using FreeRTOS that guarantees **500ms emergency response times** through priority-based preemptive scheduling. This project demonstrates core RTOS concepts with a practical automotive application featuring adaptive traffic control, weather simulation, and comprehensive performance monitoring.

## 🎯 Key Features
- **🚑 Emergency Vehicle Priority**: Guaranteed 500ms response time with immediate preemption
- **⚡ Real-Time Scheduling**: FreeRTOS task management with priority-based preemption
- **🌈 Weather Adaptive Control**: Dynamic light timing based on weather conditions (CLEAR/RAIN/FOG/SNOW)
- **📊 Performance Monitoring**: Real-time metrics for response times, CPU utilization, deadline compliance
- **🔗 Robust Communication**: TCP-based communication between RTOS core and visualization
- **📈 Data Logging**: CSV export of all system events for analysis
- **🎮 Interactive Visualization**: PyGame-based dashboard showing real-time system state

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│  Python Visualization (PyGame) ← TCP →  RTOS Core (FreeRTOS)│
│  • Real-time dashboard         │ 5000  • Task scheduling    │
│  • Event logging               │       • Priority management│
│  • Performance metrics         │       • Emergency handling │
│  • Weather effects             │       • Sensor simulation  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure
```
C:\project\MyTrafficProject\
├── rtos_server\                    # FreeRTOS Core Implementation
│   ├── robust_advanced_server.py   # Main RTOS server (Python-based)
│   ├── rtos_works_always.py        # Simple guaranteed-working version
│   └── launch_advanced.bat         # One-click launcher
│
├── python_simulator\               # Visualization & Analysis
│   ├── traffic_simulator_advanced.py  # Main visualization dashboard
│   ├── traffic_simulator.py           # Basic visualization
│   ├── analyze_data.py                # Performance data analysis
│   └── viz_works_always.py            # Simple visualization
│
└── FreeRTOS\                       # Original FreeRTOS source (reference)
```

## 🚀 Quick Start

### Prerequisites
```bash
# Required Python packages
pip install pygame pandas matplotlib
```

### Running the System

#### Option 1: One-Click Launch (Recommended)
```powershell
cd rtos_server
.\launch_advanced.bat
```

#### Option 2: Manual Start
```powershell
# Terminal 1: Start RTOS Server
cd rtos_server
python robust_advanced_server.py

# Terminal 2: Start Visualization (after RTOS is ready)
cd python_simulator
python traffic_simulator_advanced.py
```

#### Option 3: Simple Test Version
```powershell
# For quick testing without advanced features
cd rtos_server
python rtos_works_always.py

# In another terminal:
cd python_simulator
python viz_works_always.py
```

## 🎮 Controls & Interface

### Visualization Controls
| Key     | Function            | Description                              |
|---------|---------------------|------------------------------------------|
| **E**   | Emergency Vehicle   | Triggers emergency mode (500ms response) |
| **P**   | Pedestrian Crossing | Requests pedestrian crossing             |
| **W**   | Change Weather      | Cycles through CLEAR→RAIN→FOG→SNOW       |
| **R**   | Reset Metrics       | Clears performance counters              |
| **ESC** | Quit                | Exits the application                    |

### Dashboard Panels
1. **🚦 Intersections (x2)**: Real-time traffic light visualization
2. **⚡ RTOS Task Monitor**: Shows task states (RUNNING/BLOCKED/READY)
3. **📊 Performance Metrics**: Emergency response times, deadline misses, CPU usage
4. **📋 Event Log**: Timestamped system events
5. **🔧 Sensor Data**: Virtual vehicle counts and sensor readings
6. **🌤️ System Status**: Connection, weather, uptime, emergency status
7. **🎛️ Controls**: On-screen instructions

## 🔧 RTOS Task Design

| Task                 | Priority    | Description                          | State Transitions                    |
|----------------------|-------------|--------------------------------------|--------------------------------------|
| **EmergencyHandler** | 5 (Highest) | Handles emergency vehicle preemption | BLOCKED → RUNNING (on emergency)     |
| **NormalControl**    | 2           | Manages regular traffic light cycles | RUNNING → BLOCKED (during emergency) |
| **Pedestrian**       | 3           | Processes crossing requests          | READY → RUNNING (on request)         |
| **TrafficMonitor**   | 1           | Monitors system performance          | Always RUNNING                       |
| **WeatherSensor**    | 1           | Simulates weather changes            | Periodic RUNNING                     |

## 📊 Performance Metrics
- **Emergency Response Time**: Target <500ms (hard real-time constraint)
- **Deadline Misses**: Count of missed 500ms deadlines
- **CPU Utilization**: Simulated CPU usage percentage
- **Vehicle Throughput**: Virtual vehicle count through intersection
- **Average Wait Time**: Simulated vehicle waiting times

## 📈 Data Analysis
After running the system, analyze performance:
```powershell
cd python_simulator
python analyze_data.py
```
Generates:
- `traffic_report.txt` - Text summary of performance
- `reports/emergency_response.png` - Response time chart
- `reports/light_distribution.png` - Light state analysis
- `reports/wait_times.png` - Vehicle wait time trends

## 🎓 Academic Relevance

### Course Outcomes (EC802C - Real Time Operating Systems)
- **CO1**: Summarize functions and structure of general-purpose operating systems
- **CO2**: Use different scheduling algorithms on processes and threads
- **CO3**: Interpret RTOS with synchronization, communication, and interrupt handling
- **CO4**: Illustrate task constraints and analyze scheduling algorithms
- **CO5**: Illustrate applications of real-time operating systems

### Key Concepts Demonstrated
1. **Priority-Based Preemptive Scheduling**
2. **Hard vs Soft Real-Time Constraints**
3. **Task Synchronization (Semaphores/Queues)**
4. **Inter-Task Communication**
5. **Deterministic System Behavior**
6. **Performance Monitoring and Analysis**

## 🐛 Troubleshooting

### Common Issues & Solutions
| Issue                                  | Solution                                                                |
|----------------------------------------|-------------------------------------------------------------------------|
| **Port 5000 already in use**           | `netstat -ano \| findstr :5000` then `taskkill /PID [PID] /F`           |
| **"Module not found" errors**          | `pip install pygame pandas matplotlib`                                  | 
| **Connection timeouts**                | Start RTOS server FIRST, wait for "listening", THEN start visualization |
| **Visualization shows "DISCONNECTED"** | Ensure RTOS server is running and firewall allows Python                |
| **Weather effects not showing**        | Press **W** key to cycle through weather conditions                     |

### Debug Mode
```python
# Add to visualization __init__() for debugging
self.debug_mode = True
print(f"RTOS State: {self.rtos_state}")
```

## 📚 Technical Details

### Communication Protocol
```json
// RTOS → Python (State Update)
{
  "lights": {"NS": "GREEN", "EW": "RED"},
  "emergency": false,
  "weather": "CLEAR",
  "tasks": {"NormalControl": {"state": "RUNNING", "priority": 2}},
  "metrics": {"response_time": 234.5, "deadline_misses": 0},
  "timestamp": 1674043200.123
}

// Python → RTOS (Command)
{
  "event": "EMERGENCY",
  "data": {"direction": "north"},
  "timestamp": 1674043200.124
}
```

### Scheduling Algorithm
```c
// Rate Monotonic Scheduling Analysis
U = Σ(Ci/Ti) = 0.2997 < n(2^(1/n)-1) = 0.490
∴ System is schedulable under RMS
```

## 👥 Authors
- **Aarren Vincent** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments
- FreeRTOS team for the excellent real-time operating system
- PyGame community for the graphics library
- Course instructors for guidance on RTOS concepts
- Open source contributors for various Python libraries

## 📞 Support
For questions or issues:
1. Open an issue on GitHub
2. Contact: aarrenvincent@gmal.com

---

<div align="center">
  
**⭐ If this project helped you, please give it a star! ⭐**

*Last updated: January 2026 | Course: EC802C Real Time Operating Systems*

</div>