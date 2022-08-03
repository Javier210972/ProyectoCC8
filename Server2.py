import socket
import threading
import sys
import json
import pickle

IP = "ec2-52-91-210-59.compute-1.amazonaws.com"
PORT = 12345
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
# test cases for jsonStringA and jsonStringB according to your data input
jsonStringA = '[{"playerNumber" : 1,"name": "Ricardo","color" : "RED","isAlive" : true,"positionX" : -9,"positionY" : -1}, {"playerNumber" : 2,"name": "Axel","color" : "BLUE","isAlive" : true,"positionX" : 7,"positionY" : 6}]'
#jsonStringB = '{"error_1":"valueA","EEEEE":"valueC"}'
#jsonStringC = '{}'

# now we have two json STRINGS
#dictA = json.loads(jsonStringA)
#dictB = json.loads(jsonStringB)
#dictC = json.loads(jsonStringC)
#dictC.update(dictB)
#dictC.update(dictA)
mensaje = ""
##merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}
#print(dictC)

def handle_client(conn, addr):
    global mensaje
    global jsonStringA
    print(f"[NEW CONNECTION] {addr} connected.")
    #print(mensaje)
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        msg = f"{msg}"
        mensaje = msg + mensaje
        #msg = "hola"
        m ='{"Player": 1, "Posx": 5}'
        #jsonResult = {"first":"You're", "second":"Awsome!"}
        #jsonResult = json.dumps(dictC)
       
        conn.send(jsonStringA.encode(FORMAT))

    conn.close()

def main():
    #jsonresponse = json.load('{}')
    
    print("[STARTING] Server is starting aws?...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()