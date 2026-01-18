# Save as viz_works_always.py
import pygame, socket, json, threading, time

class WorkingViz:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.lights = {"NS": "RED", "EW": "GREEN"}
        self.connected = False
        
        threading.Thread(target=self.rtos_loop, daemon=True).start()
    
    def rtos_loop(self):
        while True:
            try:
                s = socket.socket()
                s.settimeout(5)
                s.connect(('127.0.0.1', 5000))
                s.settimeout(0.1)
                self.connected = True
                print("Connected to RTOS!")
                
                while True:
                    try:
                        data = s.recv(1024)
                        if data:
                            state = json.loads(data.decode())
                            self.lights = state['lights']
                    except socket.timeout:
                        pass
                    except:
                        break
            except:
                self.connected = False
                print("Connecting to RTOS...")
                time.sleep(2)
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Draw
            self.screen.fill((240, 240, 240))
            
            # Draw lights
            colors = {"RED": (255,0,0), "GREEN": (0,255,0), "YELLOW": (255,255,0)}
            
            # NS Light
            pygame.draw.circle(self.screen, colors[self.lights["NS"]], (200, 300), 50)
            pygame.draw.rect(self.screen, (100,100,100), (185, 350, 30, 100))
            
            # EW Light
            pygame.draw.circle(self.screen, colors[self.lights["EW"]], (600, 300), 50)
            pygame.draw.rect(self.screen, (100,100,100), (585, 350, 30, 100))
            
            # Status
            font = pygame.font.SysFont(None, 36)
            status = "CONNECTED" if self.connected else "DISCONNECTED"
            color = (0,200,0) if self.connected else (200,0,0)
            text = font.render(f"RTOS: {status}", True, color)
            self.screen.blit(text, (300, 50))
            
            pygame.display.flip()
            clock.tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    print("Starting visualization...")
    print("Make sure RTOS server is running first!")
    viz = WorkingViz()
    viz.run()