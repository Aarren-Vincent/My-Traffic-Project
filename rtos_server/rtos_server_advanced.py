"""
ROBUST ADVANCED RTOS SERVER - Built on working foundation
"""
import socket
import json
import time
import threading
import random
from datetime import datetime

class RobustRTOS:
    def __init__(self):
        self.lights = {"NS": "GREEN", "EW": "RED"}
        self.emergency = False
        self.weather = "CLEAR"
        self.start_time = time.time()
        
        # RTOS Tasks
        self.tasks = {
            "NormalControl": {"state": "RUNNING", "priority": 2},
            "EmergencyHandler": {"state": "BLOCKED", "priority": 5},
            "Pedestrian": {"state": "READY", "priority": 3},
            "TrafficMonitor": {"state": "RUNNING", "priority": 1}
        }
        
        # Virtual Sensors
        self.sensors = {
            "vehicle_count_ns": 12,
            "vehicle_count_ew": 8,
            "pedestrian_button_ns": False,
            "pedestrian_button_ew": False,
            "ambient_light": 85
        }
        
        # Performance Metrics
        self.metrics = {
            "emergency_response_time": 0.0,
            "cpu_utilization": 45.2,
            "deadline_misses": 0,
            "vehicle_throughput": 20
        }
        
        # Configuration
        self.emergency_deadline = 500  # 500ms
        
        print("="*70)
        print("ROBUST RTOS TRAFFIC CONTROL SYSTEM")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def get_system_state(self):
        """Get complete system state"""
        # Auto-cycle lights when not in emergency
        if not self.emergency:
            cycle_time = int(time.time()) % 30
            if cycle_time < 15:
                self.lights = {"NS": "GREEN", "EW": "RED"}
                self.tasks["NormalControl"]["state"] = "RUNNING"
            elif cycle_time < 18:
                self.lights = {"NS": "YELLOW", "EW": "RED"}
            elif cycle_time < 30:
                self.lights = {"NS": "RED", "EW": "GREEN"}
        
        # Update sensor data
        if self.lights["NS"] == "GREEN":
            self.sensors["vehicle_count_ns"] = max(0, self.sensors["vehicle_count_ns"] - random.randint(0, 2))
            self.sensors["vehicle_count_ew"] = min(20, self.sensors["vehicle_count_ew"] + random.randint(0, 1))
        else:
            self.sensors["vehicle_count_ew"] = max(0, self.sensors["vehicle_count_ew"] - random.randint(0, 2))
            self.sensors["vehicle_count_ns"] = min(20, self.sensors["vehicle_count_ns"] + random.randint(0, 1))
        
        return {
            "lights": self.lights,
            "emergency": self.emergency,
            "weather": self.weather,
            "time_of_day": "DAY" if 6 <= datetime.now().hour < 18 else "NIGHT",
            "tasks": self.tasks,
            "sensors": self.sensors,
            "metrics": self.metrics,
            "system_health": {
                "uptime": round(time.time() - self.start_time, 1),
                "connection_stable": True
            },
            "timestamp": time.time()
        }
    
    def handle_emergency(self):
        """Handle emergency vehicle"""
        emergency_start = time.time()
        
        # Record task states before emergency
        old_states = {k: v["state"] for k, v in self.tasks.items()}
        
        # Change states
        self.emergency = True
        self.lights = {"NS": "GREEN", "EW": "RED"}
        self.tasks["NormalControl"]["state"] = "BLOCKED"
        self.tasks["EmergencyHandler"]["state"] = "RUNNING"
        
        # Calculate response time
        response_time = (time.time() - emergency_start) * 1000  # ms
        self.metrics["emergency_response_time"] = response_time
        
        # Check deadline
        if response_time > self.emergency_deadline:
            self.metrics["deadline_misses"] += 1
        
        print(f"🚑 EMERGENCY! Response: {response_time:.1f}ms | "
              f"Deadline: {self.emergency_deadline}ms | "
              f"Misses: {self.metrics['deadline_misses']}")
        
        # Auto-clear after 10 seconds
        def clear_emergency():
            if self.emergency:  # Check if still in emergency
                self.emergency = False
                self.tasks["NormalControl"]["state"] = "RUNNING"
                self.tasks["EmergencyHandler"]["state"] = "BLOCKED"
                print("✅ Emergency cleared, normal operation resumed")
        
        threading.Timer(10.0, clear_emergency).start()
        
        return response_time
    
    def handle_pedestrian(self):
        """Handle pedestrian crossing request"""
        print("🚶 Pedestrian crossing activated")
        self.lights = {"NS": "RED", "EW": "RED"}
        self.tasks["Pedestrian"]["state"] = "RUNNING"
        
        # Auto-clear after 5 seconds
        def clear_pedestrian():
            self.tasks["Pedestrian"]["state"] = "READY"
            self.lights = {"NS": "GREEN", "EW": "RED"}
            print("✅ Pedestrian crossing complete")
        
        threading.Timer(5.0, clear_pedestrian).start()
    
    def handle_weather_change(self, new_weather):
        """Change weather condition"""
        valid_weather = ["CLEAR", "RAIN", "FOG", "SNOW"]
        if new_weather in valid_weather:
            self.weather = new_weather
            print(f"🌤️  Weather changed to: {new_weather}")
    
    def start_server(self, port=5000):
        """Start the robust RTOS server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(1)
        
        print(f"📡 Server listening on port {port}")
        print("💡 Commands from visualization:")
        print("   E = Emergency vehicle")
        print("   P = Pedestrian crossing")
        print("   W = Change weather")
        print("   R = Reset metrics")
        print("-" * 70)
        
        while True:
            try:
                # Accept connection
                client, addr = server.accept()
                client.settimeout(0.1)  # Short timeout for recv
                print(f"✅ Visualization connected: {addr}")
                
                # Main communication loop
                while True:
                    try:
                        # Check for incoming commands
                        try:
                            data = client.recv(1024)
                            if data:
                                try:
                                    cmd = json.loads(data.decode())
                                    event = cmd.get('event', '').upper()
                                    
                                    if event == 'EMERGENCY':
                                        self.handle_emergency()
                                    elif event == 'PEDESTRIAN':
                                        self.handle_pedestrian()
                                    elif event == 'CHANGE_WEATHER':
                                        new_weather = cmd.get('data', {}).get('weather', 'CLEAR')
                                        self.handle_weather_change(new_weather)
                                    elif event == 'RESET_METRICS':
                                        self.metrics['deadline_misses'] = 0
                                        print("📊 Metrics reset")
                                    
                                except json.JSONDecodeError:
                                    pass
                        except socket.timeout:
                            pass  # No data yet
                        
                        # Send current state
                        state = self.get_system_state()
                        client.send((json.dumps(state) + "\n").encode())
                        
                        # Small delay
                        time.sleep(0.1)
                        
                    except (ConnectionResetError, BrokenPipeError):
                        print(f"📭 Visualization disconnected")
                        break
                    except Exception as e:
                        print(f"⚠️  Communication error: {e}")
                        break
                
                # Cleanup
                client.close()
                print("🔄 Waiting for reconnection...")
                
            except KeyboardInterrupt:
                print("\n🛑 Server shutdown requested")
                break
            except Exception as e:
                print(f"💥 Server error: {e}")
                time.sleep(1)  # Wait before retrying
        
        server.close()
        print("👋 Server stopped")

if __name__ == "__main__":
    rtos = RobustRTOS()
    rtos.start_server(port=5000)