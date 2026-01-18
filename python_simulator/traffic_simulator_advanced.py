"""
ADVANCED TRAFFIC VISUALIZATION WITH WEATHER EFFECTS
"""
import pygame
import socket
import json
import threading
import time
from datetime import datetime

class AdvancedTrafficVisualization:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 900))
        pygame.display.set_caption("RTOS Traffic Control - WITH WEATHER")
        
        # Colors - ADDED WEATHER COLORS
        self.colors = {
            'RED': (255, 50, 50),
            'YELLOW': (255, 255, 100),
            'GREEN': (100, 255, 100),
            'ROAD': (60, 60, 60),
            'PANEL_BG': (250, 250, 250),
            'PANEL_BORDER': (200, 200, 200),
            'TEXT': (30, 30, 30),
            'WARNING': (255, 150, 0),
            'DANGER': (255, 50, 50),
            'SUCCESS': (50, 200, 50),
            'EMERGENCY_BG': (255, 230, 230)
        }
        
        # WEATHER COLORS - ADDED BACK
        self.weather_colors = {
            'CLEAR': (135, 206, 235),    # Sky blue
            'RAIN': (100, 100, 120),     # Gray
            'FOG': (200, 200, 200),      # Light gray
            'SNOW': (220, 240, 255),     # Snow white
            'UNKNOWN': (240, 240, 240)   # Default
        }
        
        # Fonts
        self.fonts = {
            'large': pygame.font.SysFont('Consolas', 28, bold=True),
            'medium': pygame.font.SysFont('Consolas', 20),
            'small': pygame.font.SysFont('Consolas', 16),
            'tiny': pygame.font.SysFont('Consolas', 14)
        }
        
        # RTOS Connection
        self.rtos_state = {
            "lights": {"NS": "RED", "EW": "GREEN"},
            "emergency": False,
            "weather": "CLEAR",  # Default weather
            "tasks": {},
            "sensors": {},
            "metrics": {}
        }
        self.rtos_socket = None
        self.connected = False
        self.last_state_update = 0
        
        # Event indicators
        self.event_messages = []
        self.last_emergency_time = 0
        self.last_pedestrian_time = 0
        
        # Weather animation
        self.weather_particles = []
        self.last_weather_update = 0
        
        # Initialize
        self.setup_rtos_connection()
        self.setup_ui_elements()
        
        print("🌈 Visualization with WEATHER EFFECTS Started")
        print("   Controls: E=Emergency, P=Pedestrian, W=Weather, R=Reset")
        print("   Weather colors: Blue=CLEAR, Gray=RAIN, White=SNOW")
    
    def setup_rtos_connection(self):
        """Setup connection to RTOS server"""
        self.comm_thread = threading.Thread(target=self.rtos_communication, daemon=True)
        self.comm_thread.start()
    
    def rtos_communication(self):
        """Background thread for RTOS communication"""
        while True:
            try:
                if not self.connected or self.rtos_socket is None:
                    print("🔌 Connecting to RTOS...")
                    self.rtos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.rtos_socket.settimeout(5.0)
                    self.rtos_socket.connect(('127.0.0.1', 5000))
                    self.rtos_socket.settimeout(0.1)
                    self.connected = True
                    print("✅ Connected to RTOS!")
                    self.add_event_message("Connected to RTOS", "SUCCESS")
                
                # Send heartbeat
                current_time = time.time()
                if current_time - self.last_state_update > 10:
                    try:
                        heartbeat = {'event': 'HEARTBEAT', 'timestamp': current_time}
                        self.rtos_socket.send(json.dumps(heartbeat).encode())
                    except:
                        self.connected = False
                        self.rtos_socket = None
                        continue
                
                # Receive data
                try:
                    data = self.rtos_socket.recv(65536).decode()
                    if data:
                        lines = data.strip().split('\n')
                        for line in lines:
                            if line:
                                try:
                                    new_state = json.loads(line)
                                    self.rtos_state.update(new_state)
                                    self.last_state_update = current_time
                                    
                                    # Check for weather change
                                    old_weather = self.rtos_state.get('weather', 'CLEAR')
                                    new_weather = new_state.get('weather', old_weather)
                                    if new_weather != old_weather:
                                        self.add_event_message(f"Weather changed to: {new_weather}", "INFO")
                                        self.generate_weather_particles(new_weather)
                                    
                                    # Check for emergency
                                    if new_state.get('emergency', False) and not self.rtos_state.get('last_emergency', False):
                                        self.add_event_message("🚑 EMERGENCY VEHICLE!", "DANGER")
                                        self.last_emergency_time = current_time
                                    
                                    # Check for pedestrian
                                    tasks = new_state.get('tasks', {})
                                    if tasks.get('Pedestrian', {}).get('state') == 'RUNNING':
                                        if current_time - self.last_pedestrian_time > 1:
                                            self.add_event_message("🚶 PEDESTRIAN CROSSING", "WARNING")
                                            self.last_pedestrian_time = current_time
                                    
                                    self.rtos_state['last_emergency'] = new_state.get('emergency', False)
                                    
                                except json.JSONDecodeError:
                                    pass
                except socket.timeout:
                    pass
                    
            except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError):
                if self.connected:
                    self.add_event_message("RTOS Disconnected", "DANGER")
                self.connected = False
                self.rtos_socket = None
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Communication error: {e}")
                time.sleep(1)
    
    def generate_weather_particles(self, weather):
        """Generate particles based on weather"""
        self.weather_particles = []
        current_time = time.time()
        
        if weather == "RAIN":
            # Rain drops
            for _ in range(100):
                self.weather_particles.append({
                    'x': pygame.time.get_ticks() % 1400,  # Random start
                    'y': -10,
                    'speed': 8 + pygame.time.get_ticks() % 5,
                    'type': 'rain'
                })
        elif weather == "SNOW":
            # Snow flakes
            for _ in range(50):
                self.weather_particles.append({
                    'x': pygame.time.get_ticks() % 1400,
                    'y': -10,
                    'speed': 2 + pygame.time.get_ticks() % 2,
                    'drift': (pygame.time.get_ticks() % 10) - 5,
                    'type': 'snow'
                })
        elif weather == "FOG":
            # Fog particles
            for _ in range(30):
                self.weather_particles.append({
                    'x': pygame.time.get_ticks() % 1400,
                    'y': 100 + pygame.time.get_ticks() % 600,
                    'size': 20 + pygame.time.get_ticks() % 30,
                    'type': 'fog'
                })
        
        self.last_weather_update = current_time
    
    def update_weather_particles(self):
        """Update weather particle positions"""
        current_time = time.time()
        
        # Update existing particles
        for particle in self.weather_particles[:]:
            if particle['type'] == 'rain':
                particle['y'] += particle['speed']
                if particle['y'] > 900:
                    self.weather_particles.remove(particle)
            elif particle['type'] == 'snow':
                particle['y'] += particle['speed']
                particle['x'] += particle.get('drift', 0)
                if particle['y'] > 900 or particle['x'] < -10 or particle['x'] > 1410:
                    self.weather_particles.remove(particle)
        
        # Add new particles occasionally
        weather = self.rtos_state.get('weather', 'CLEAR')
        if weather == "RAIN" and current_time - self.last_weather_update > 0.05:
            self.weather_particles.append({
                'x': pygame.time.get_ticks() % 1400,
                'y': -10,
                'speed': 8 + pygame.time.get_ticks() % 5,
                'type': 'rain'
            })
            self.last_weather_update = current_time
        elif weather == "SNOW" and current_time - self.last_weather_update > 0.1:
            self.weather_particles.append({
                'x': pygame.time.get_ticks() % 1400,
                'y': -10,
                'speed': 2 + pygame.time.get_ticks() % 2,
                'drift': (pygame.time.get_ticks() % 10) - 5,
                'type': 'snow'
            })
            self.last_weather_update = current_time
    
    def draw_weather_particles(self, surface):
        """Draw weather particles"""
        weather = self.rtos_state.get('weather', 'CLEAR')
        
        for particle in self.weather_particles:
            if particle['type'] == 'rain':
                # Rain drop - blue line
                pygame.draw.line(surface, (100, 150, 255), 
                               (particle['x'], particle['y']),
                               (particle['x'], particle['y'] + 10), 2)
            elif particle['type'] == 'snow':
                # Snow flake - white circle
                pygame.draw.circle(surface, (255, 255, 255),
                                 (int(particle['x']), int(particle['y'])), 3)
            elif particle['type'] == 'fog':
                # Fog - semi-transparent circle
                fog_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
                pygame.draw.circle(fog_surface, (255, 255, 255, 50),
                                 (particle['size']//2, particle['size']//2),
                                 particle['size']//2)
                surface.blit(fog_surface, (particle['x'], particle['y']))
    
    def add_event_message(self, message, msg_type="INFO"):
        """Add an event message to display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_messages.insert(0, f"[{timestamp}] {message}")
        if len(self.event_messages) > 10:
            self.event_messages.pop()
        print(f"📢 {message}")
    
    def setup_ui_elements(self):
        """Setup UI panel positions"""
        self.panels = {
            'intersection1': {'rect': pygame.Rect(50, 50, 400, 400), 'title': 'INTERSECTION 1'},
            'intersection2': {'rect': pygame.Rect(500, 50, 400, 400), 'title': 'INTERSECTION 2'},
            'rtos_tasks': {'rect': pygame.Rect(950, 50, 400, 250), 'title': 'RTOS TASK MONITOR'},
            'performance': {'rect': pygame.Rect(950, 320, 400, 200), 'title': 'PERFORMANCE'},
            'events': {'rect': pygame.Rect(50, 470, 400, 350), 'title': 'EVENT LOG'},
            'sensors': {'rect': pygame.Rect(500, 470, 400, 200), 'title': 'SENSORS'},
            'controls': {'rect': pygame.Rect(500, 690, 400, 130), 'title': 'CONTROLS'},
            'status': {'rect': pygame.Rect(950, 540, 400, 280), 'title': 'SYSTEM STATUS'}
        }
    
    def get_background_color(self):
        """Get background color based on weather and emergency"""
        weather = self.rtos_state.get('weather', 'CLEAR')
        
        if self.rtos_state.get('emergency', False):
            # Emergency overrides weather - red tint
            base_color = self.weather_colors.get(weather, self.weather_colors['UNKNOWN'])
            # Blend with emergency red
            return tuple(min(255, int(c * 0.7 + 255 * 0.3)) for c in base_color)
        else:
            # Normal weather color
            return self.weather_colors.get(weather, self.weather_colors['UNKNOWN'])
    
    def draw_panel(self, surface, rect, title, color=None):
        """Draw a UI panel"""
        if color is None:
            color = self.colors['PANEL_BG']
        
        # Semi-transparent panel for weather visibility
        panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (*color, 200), (0, 0, rect.width, rect.height), border_radius=8)
        pygame.draw.rect(panel_surface, (*self.colors['PANEL_BORDER'], 200), 
                        (0, 0, rect.width, rect.height), 2, border_radius=8)
        surface.blit(panel_surface, rect)
        
        # Title
        title_rect = pygame.Rect(rect.x, rect.y - 25, rect.width, 25)
        pygame.draw.rect(surface, self.colors['PANEL_BORDER'], title_rect, border_radius=8)
        title_text = self.fonts['small'].render(title, True, self.colors['TEXT'])
        surface.blit(title_text, (rect.x + 10, rect.y - 22))
    
    def draw_intersection(self, surface, rect, lights, emergency=False):
        """Draw an intersection with lights"""
        center_x = rect.x + rect.width // 2
        center_y = rect.y + rect.height // 2
        
        # Background tint for emergency (semi-transparent)
        if emergency:
            emergency_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(emergency_surface, (255, 200, 200, 100), 
                           (0, 0, rect.width, rect.height), border_radius=8)
            surface.blit(emergency_surface, rect)
        
        # Roads
        pygame.draw.rect(surface, self.colors['ROAD'], 
                        (rect.x + 50, center_y - 15, rect.width - 100, 30))
        pygame.draw.rect(surface, self.colors['ROAD'], 
                        (center_x - 15, rect.y + 50, 30, rect.height - 100))
        
        # Lane markings
        for i in range(rect.x + 60, rect.x + rect.width - 40, 40):
            pygame.draw.rect(surface, (255, 255, 255), (i, center_y - 5, 20, 3))
            pygame.draw.rect(surface, (255, 255, 255), (center_x - 5, i - rect.x + 50, 3, 20))
        
        # Traffic lights
        light_positions = [
            (center_x - 120, center_y, 'EW'),
            (center_x + 120, center_y, 'EW'),
            (center_x, center_y - 120, 'NS'),
            (center_x, center_y + 120, 'NS')
        ]
        
        for x, y, direction in light_positions:
            self.draw_traffic_light(surface, x, y, direction, lights.get(direction, 'RED'))
        
        # Emergency indicator
        if emergency:
            warning_text = self.fonts['medium'].render("🚑 EMERGENCY", True, self.colors['DANGER'])
            surface.blit(warning_text, (center_x - 60, rect.y + 20))
    
    def draw_traffic_light(self, surface, x, y, direction, state):
        """Draw a traffic light"""
        # Pole
        pygame.draw.rect(surface, (100, 100, 100), (x - 5, y - 60, 10, 60))
        
        # Light box
        light_box = pygame.Rect(x - 25, y - 100, 50, 80)
        pygame.draw.rect(surface, (50, 50, 50), light_box, border_radius=4)
        pygame.draw.rect(surface, (30, 30, 30), light_box, 2, border_radius=4)
        
        # Lights
        light_states = ['RED', 'YELLOW', 'GREEN']
        for i, light_state in enumerate(light_states):
            light_y = y - 80 + i * 25
            if state == light_state:
                color = self.colors[light_state]
                # Add glow
                pygame.draw.circle(surface, 
                                 tuple(min(255, c + 50) for c in color),
                                 (x, light_y), 8)
            else:
                color = (40, 40, 40)
            
            pygame.draw.circle(surface, color, (x, light_y), 6)
    
    def draw_rtos_tasks(self, surface, rect, tasks):
        """Draw RTOS task states"""
        y = rect.y + 20
        for task_name, task_info in tasks.items():
            state = task_info.get('state', 'UNKNOWN')
            priority = task_info.get('priority', 0)
            
            # Color based on state
            if state == 'RUNNING':
                color = self.colors['SUCCESS']
            elif state == 'BLOCKED':
                color = self.colors['DANGER']
            elif state == 'READY':
                color = self.colors['WARNING']
            else:
                color = self.colors['TEXT']
            
            # Task text
            task_text = f"{task_name:20} {state:10} P:{priority}"
            text_surface = self.fonts['small'].render(task_text, True, color)
            surface.blit(text_surface, (rect.x + 10, y))
            y += 25
    
    def draw_performance_metrics(self, surface, rect, metrics):
        """Draw performance metrics"""
        if not metrics:
            return
        
        y = rect.y + 20
        
        # Emergency response time
        response_time = metrics.get('emergency_response_time', 0)
        response_text = f"Response: {response_time:.1f}ms"
        response_color = self.colors['SUCCESS'] if response_time <= 500 else self.colors['DANGER']
        text_surface = self.fonts['small'].render(response_text, True, response_color)
        surface.blit(text_surface, (rect.x + 10, y))
        y += 25
        
        # Deadline misses
        misses = metrics.get('deadline_misses', 0)
        misses_text = f"Deadline Misses: {misses}"
        misses_color = self.colors['DANGER'] if misses > 0 else self.colors['TEXT']
        misses_surface = self.fonts['small'].render(misses_text, True, misses_color)
        surface.blit(misses_surface, (rect.x + 10, y))
        y += 25
        
        # CPU Utilization
        cpu = metrics.get('cpu_utilization', 0)
        cpu_text = f"CPU: {cpu:.1f}%"
        cpu_surface = self.fonts['small'].render(cpu_text, True, self.colors['TEXT'])
        surface.blit(cpu_surface, (rect.x + 10, y))
    
    def draw_event_log(self, surface, rect):
        """Draw event log messages"""
        y = rect.y + 20
        for i, message in enumerate(self.event_messages[:8]):
            text_surface = self.fonts['tiny'].render(message, True, self.colors['TEXT'])
            surface.blit(text_surface, (rect.x + 10, y))
            y += 22
    
    def draw_sensors(self, surface, rect, sensors):
        """Draw sensor data"""
        if not sensors:
            return
        
        y = rect.y + 20
        
        # Vehicle counts
        vehicles_ns = sensors.get('vehicle_count_ns', 0)
        vehicles_ew = sensors.get('vehicle_count_ew', 0)
        
        vehicles_text = f"Vehicles NS: {vehicles_ns}"
        text_surface = self.fonts['small'].render(vehicles_text, True, self.colors['TEXT'])
        surface.blit(text_surface, (rect.x + 10, y))
        y += 25
        
        vehicles_text = f"Vehicles EW: {vehicles_ew}"
        text_surface = self.fonts['small'].render(vehicles_text, True, self.colors['TEXT'])
        surface.blit(text_surface, (rect.x + 10, y))
    
    def draw_controls(self, surface, rect):
        """Draw control instructions"""
        y = rect.y + 20
        
        controls = [
            "CONTROLS:",
            "E - Trigger Emergency Vehicle",
            "P - Pedestrian Crossing",
            "W - Change Weather (Cycle)",
            "R - Reset Metrics",
            "ESC - Quit"
        ]
        
        for control in controls:
            text_surface = self.fonts['small'].render(control, True, self.colors['TEXT'])
            surface.blit(text_surface, (rect.x + 10, y))
            y += 22
    
    def draw_status(self, surface, rect, system_state):
        """Draw system status"""
        y = rect.y + 20
        
        # Connection status
        status = "CONNECTED" if self.connected else "DISCONNECTED"
        status_color = self.colors['SUCCESS'] if self.connected else self.colors['DANGER']
        status_text = f"RTOS: {status}"
        status_surface = self.fonts['medium'].render(status_text, True, status_color)
        surface.blit(status_surface, (rect.x + 10, y))
        y += 30
        
        # Emergency status
        emergency = system_state.get('emergency', False)
        emergency_text = "🚑 EMERGENCY ACTIVE" if emergency else "✅ Normal Operation"
        emergency_color = self.colors['DANGER'] if emergency else self.colors['SUCCESS']
        emergency_surface = self.fonts['small'].render(emergency_text, True, emergency_color)
        surface.blit(emergency_surface, (rect.x + 10, y))
        y += 25
        
        # Weather with color indicator
        weather = system_state.get('weather', 'CLEAR')
        weather_text = f"Weather: {weather}"
        weather_surface = self.fonts['small'].render(weather_text, True, self.colors['TEXT'])
        surface.blit(weather_surface, (rect.x + 10, y))
        
        # Weather color indicator box
        weather_color = self.weather_colors.get(weather, self.weather_colors['UNKNOWN'])
        pygame.draw.rect(surface, weather_color, (rect.x + 120, y, 20, 20))
        pygame.draw.rect(surface, self.colors['TEXT'], (rect.x + 120, y, 20, 20), 1)
        y += 30
        
        # Uptime
        uptime = system_state.get('system_health', {}).get('uptime', 0)
        uptime_text = f"Uptime: {uptime:.0f}s"
        uptime_surface = self.fonts['small'].render(uptime_text, True, self.colors['TEXT'])
        surface.blit(uptime_surface, (rect.x + 10, y))
    
    def send_command(self, event, data=None):
        """Send command to RTOS server"""
        if not self.connected or self.rtos_socket is None:
            self.add_event_message(f"Cannot send {event}: Not connected", "DANGER")
            return False
            
        command = {'event': event}
        if data:
            command['data'] = data
            
        try:
            self.rtos_socket.send(json.dumps(command).encode())
            self.add_event_message(f"Sent: {event}", "INFO")
            return True
        except Exception as e:
            self.add_event_message(f"Failed to send {event}: {e}", "DANGER")
            self.connected = False
            return False
    
    def run(self):
        """Main simulation loop"""
        clock = pygame.time.Clock()
        running = True
        
        print("\n🌈 Visualization with WEATHER ready!")
        print("   Press W to cycle through weather effects")
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_e:
                        self.send_command('EMERGENCY')
                    elif event.key == pygame.K_p:
                        self.send_command('PEDESTRIAN')
                    elif event.key == pygame.K_w:
                        # Cycle weather
                        weathers = ['CLEAR', 'RAIN', 'FOG', 'SNOW']
                        current = self.rtos_state.get('weather', 'CLEAR')
                        next_index = (weathers.index(current) + 1) % len(weathers) if current in weathers else 0
                        self.send_command('CHANGE_WEATHER', {'weather': weathers[next_index]})
                        print(f"🌤️  Requesting weather: {weathers[next_index]}")
                    elif event.key == pygame.K_r:
                        self.send_command('RESET_METRICS')
            
            # Clear screen with WEATHER COLOR
            bg_color = self.get_background_color()
            self.screen.fill(bg_color)
            
            # Update and draw weather particles
            self.update_weather_particles()
            self.draw_weather_particles(self.screen)
            
            # Draw all panels (semi-transparent)
            for panel_name, panel_info in self.panels.items():
                self.draw_panel(self.screen, panel_info['rect'], panel_info['title'])
            
            # Draw panel contents
            emergency = self.rtos_state.get('emergency', False)
            
            # Intersections
            self.draw_intersection(self.screen, self.panels['intersection1']['rect'], 
                                 self.rtos_state.get('lights', {}), emergency)
            self.draw_intersection(self.screen, self.panels['intersection2']['rect'], 
                                 self.rtos_state.get('lights', {}), emergency)
            
            # RTOS Tasks
            tasks = self.rtos_state.get('tasks', {})
            self.draw_rtos_tasks(self.screen, self.panels['rtos_tasks']['rect'], tasks)
            
            # Performance Metrics
            metrics = self.rtos_state.get('metrics', {})
            self.draw_performance_metrics(self.screen, self.panels['performance']['rect'], metrics)
            
            # Event Log
            self.draw_event_log(self.screen, self.panels['events']['rect'])
            
            # Sensors
            sensors = self.rtos_state.get('sensors', {})
            self.draw_sensors(self.screen, self.panels['sensors']['rect'], sensors)
            
            # Controls
            self.draw_controls(self.screen, self.panels['controls']['rect'])
            
            # Status
            self.draw_status(self.screen, self.panels['status']['rect'], self.rtos_state)
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        # Cleanup
        if self.rtos_socket:
            try:
                self.rtos_socket.close()
            except:
                pass
        pygame.quit()
        print("\n👋 Visualization stopped")

if __name__ == "__main__":
    print("="*60)
    print("ADVANCED TRAFFIC VISUALIZATION WITH WEATHER EFFECTS")
    print("="*60)
    print("\n⚠️  Make sure RTOS server is running first!")
    print("   Command: python robust_advanced_server.py")
    print("="*60)
    
    viz = AdvancedTrafficVisualization()
    viz.run()