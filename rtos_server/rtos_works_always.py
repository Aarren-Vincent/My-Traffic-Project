# Save as rtos_works_always.py
import socket, json, time, threading

class WorkingRTOS:
    def __init__(self):
        self.lights = {"NS": "GREEN", "EW": "RED"}
        self.clients = []
        
    def start(self):
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 5000))
        server.listen(5)
        
        print("="*50)
        print("WORKING RTOS SERVER - PORT 5000")
        print("="*50)
        
        threading.Thread(target=self.light_cycle, daemon=True).start()
        
        while True:
            client, addr = server.accept()
            print(f"New client: {addr}")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
    
    def light_cycle(self):
        while True:
            time.sleep(15)
            if self.lights["NS"] == "GREEN":
                self.lights = {"NS": "YELLOW", "EW": "RED"}
                time.sleep(3)
                self.lights = {"NS": "RED", "EW": "GREEN"}
            else:
                self.lights = {"NS": "GREEN", "EW": "RED"}
    
    def handle_client(self, client):
        client.settimeout(0.1)
        while True:
            try:
                # Send state
                state = {"lights": self.lights, "timestamp": time.time()}
                client.send((json.dumps(state) + "\n").encode())
                time.sleep(0.1)
            except:
                print("Client disconnected")
                client.close()
                break

if __name__ == "__main__":
    rtos = WorkingRTOS()
    rtos.start()