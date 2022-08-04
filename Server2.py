import socket
import threading
import sys
import json
import pickle

IP = "127.0.0.1"
PORT = 1225
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

playersStatus = {
    "playerNumber0" : 0,
    "name0" : "Ricardo",
    "color0" : "BLUE",
    "isAlive0" : True,
    "positionX0" : 0,
    "positionY0" : 0,
    "animation_isAlive0" : True,
    "animation_isTouchingTheGround0" : True,

    "playerNumber1" : 1,
    "name1" : "Ghost",
    "color1" : "BLACK",
    "isAlive1" : True,
    "positionX1" : -3,
    "positionY1" : -3,
    "animation_isAlive1" : True,
    "animation_isTouchingTheGround1" : True,


    "playerNumber2" : 2,
    "name2" : "Ghost2",
    "color2" : "SKYBLUE",
    "isAlive2" : True,
    "positionX2" : 3,
    "positionY2" : 3,
    "animation_isAlive2" : True,
    "animation_isTouchingTheGround2" : True,

    "playerNumber3" : -1,
    "name3" : "",
    "color3" : "",
    "isAlive3" : False,
    "positionX3" : 0,
    "positionY3" : 0,
    "animation_isAlive3" : True,
    "animation_isTouchingTheGround3" : True,

    "playerNumber4" : -1,
    "name4" : "",
    "color4" : "",
    "isAlive4" : False,
    "positionX4" : 0,
    "positionY4" : 0,
    "animation_isAlive4" : True,
    "animation_isTouchingTheGround4" : True,

    #System variables
    "sys_status" : "DISPLAYING_WINNER",
    "sys_previousWinner" : "WINNER BASE"
}    

mensaje = ""

def handle_client(conn, addr):
    global mensaje
    global playersStatus
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        #No importa
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        #No importa          

        #Print general status
        #print(playersStatus)      

        #Update general status
        print("ALL DICT")
        print(playersStatus)
        newDict = json.loads(msg);
        playerId = newDict["playerNumber"]


        playersStatus["isAlive" + str(playerId)] = newDict["isAlive"]
        playersStatus["positionX" + str(playerId)] = newDict["positionX"]
        playersStatus["positionY" + str(playerId)] = newDict["positionY"]
        playersStatus["animation_isAlive" + str(playerId)] = newDict["animation_isAlive"]
        playersStatus["animation_isTouchingTheGround" + str(playerId)] = newDict["animation_isTouchingTheGround"]

        #Reponse all players status
        toSendGeneralStatus = json.dumps(playersStatus)
        conn.send(toSendGeneralStatus.encode(FORMAT))

    conn.close()

def main():
    
    print("[STARTING] Server is starting...")
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