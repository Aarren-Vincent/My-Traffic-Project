import socket, json, time

server = socket.socket()
server.bind(('0.0.0.0', 5000))
server.listen(1)
print("Test RTOS Ready")

client, addr = server.accept()
print(f"Connected: {addr}")

lights = {"NS": "GREEN", "EW": "RED"}

while True:
    # Send state
    state = {"lights": lights}
    client.send((json.dumps(state) + "\n").encode())
    
    # Toggle lights every 5 seconds
    if int(time.time()) % 10 < 5:
        lights = {"NS": "GREEN", "EW": "RED"}
    else:
        lights = {"NS": "RED", "EW": "GREEN"}
    
    time.sleep(0.5)