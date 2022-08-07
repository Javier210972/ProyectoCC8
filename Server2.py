import socket
import threading
import sys
import json
import pickle
import random, string
import os

IP = "127.0.0.1"
PORT = 1229
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

GAME_NUMBER_OF_PLAYERS = 5;
numberOfPlayers = 0;
playersLock = threading.Lock()
restartFlag = False;

playersStatus = {
    "playerNumber0" : -1,
    "name0" : "",
    "color0" : "PURPLE",
    "isAlive0" : False,
    "positionX0" : -12,
    "positionY0" : -6,
    "animation_isAlive0" : True,
    "animation_isTouchingTheGround0" : True,

    "playerNumber1" : -1,
    "name1" : "",
    "color1" : "YELLOW",
    "isAlive1" : False,
    "positionX1" : -8,
    "positionY1" : -6,
    "animation_isAlive1" : True,
    "animation_isTouchingTheGround1" : True,


    "playerNumber2" : -1,
    "name2" : "",
    "color2" : "SKYBLUE",
    "isAlive2" : False,
    "positionX2" : 4,
    "positionY2" : -6,
    "animation_isAlive2" : True,
    "animation_isTouchingTheGround2" : True,

    "playerNumber3" : -1,
    "name3" : "",
    "color3" : "RED",
    "isAlive3" : False,
    "positionX3" : 8,
    "positionY3" : -6,
    "animation_isAlive3" : True,
    "animation_isTouchingTheGround3" : True,

    "playerNumber4" : -1,
    "name4" : "",
    "color4" : "BLUE",
    "isAlive4" : False,
    "positionX4" : 12,
    "positionY4" : -6,
    "animation_isAlive4" : True,
    "animation_isTouchingTheGround4" : True,

    #System variables
    "sys_status" : "WAITING_FOR_PLAYERS",
    "sys_previousWinner" : "WINNER BASE",
    "sys_winnerColor" : "BLACK",
    "sys_randomSeed" : 90
}    

playersHashes = []

ragnarokCounter = 0

def handle_client(conn, addr):
    global GAME_NUMBER_OF_PLAYERS
    global numberOfPlayers
    global playersLock
    global playersHashes
    global playersStatus

    global ragnarokCounter

    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:        
        #No importa
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        #No importa              

        #Update cases
        toSendAPI = ""
        if("REQUESTING_ID" in msg):
            playersLock.acquire();
            if(numberOfPlayers < (GAME_NUMBER_OF_PLAYERS)):
                playerIdToSend = str(numberOfPlayers);
                

                playersStatus["name"  + str(numberOfPlayers)] = msg.split(" ")[1];
                playersStatus["playerNumber"  + str(numberOfPlayers)] = numberOfPlayers;
                playersStatus["isAlive"  + str(numberOfPlayers)] = True;

                toSendAPI = "OK_REQUESTING_ID " + playerIdToSend  + " " + playersStatus["color"  + str(numberOfPlayers)];                
                print("Player #" + playerIdToSend +  "  -> " +  msg.split(" ")[1] + " ");
                numberOfPlayers+=1;
                
            else: 
                toSendAPI = "FULL_REQUESTING_ID";                
            playersLock.release();            

        else:
            if(playersStatus["sys_status"] != "PLAYING"):
                playersLock.acquire();
                if(numberOfPlayers < (GAME_NUMBER_OF_PLAYERS)):
                    pass;
                else:
                    playersStatus["sys_status"] = "PLAYING";
                playersLock.release();

            newDict = json.loads(msg);
            playerId = newDict["playerNumber"]
            playersStatus["isAlive" + str(playerId)] = newDict["animation_isAlive"]
            playersStatus["positionX" + str(playerId)] = newDict["positionX"]
            playersStatus["positionY" + str(playerId)] = newDict["positionY"]
            playersStatus["animation_isAlive" + str(playerId)] = newDict["animation_isAlive"]
            playersStatus["animation_isTouchingTheGround" + str(playerId)] = newDict["animation_isTouchingTheGround"]
            
            #Eval game is over
            if playersStatus["sys_status"] == "PLAYING":
                alivePlayers = 0;                    
                for i in range(5):                
                    if(playersStatus["isAlive" + str(i)]):
                                        
                        alivePlayers+=1;                            

                if(alivePlayers <= 1):
                    playersStatus["sys_status"] = "GAME_OVER";
                    
                    if(alivePlayers == 0):
                        pass;
                    else:
                        for i in range(5):
                            if(playersStatus["isAlive" + str(i)]):
                                playersStatus["sys_previousWinner"] = playersStatus["name"  + str(i)];                            
                                playersStatus["sys_winnerColor"] = playersStatus["color"  + str(i)];
                                
                                ragnarokCounter+=1;

            toSendAPI = json.dumps(playersStatus)
            #print(ragnarokCounter)
            if(ragnarokCounter > 50000):
                break;
        #Reponse all players status
        
        conn.send(toSendAPI.encode(FORMAT))
    print("[DYING] Connection close...")
    #restartServerGame()
    conn.close()

def generatePlayerHashes():
    i = 0;
    print("----------PLAYER INVITATION CODES ----------");
    while (i < 5):
        randomHash = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        if randomHash in playersHashes:
            continue;
        
        print("PLAYER " + str(i) + " -> " + randomHash)
        playersHashes.append(randomHash);
        i += 1;

def main():
    global playersStatus
    global IP
    global PORT
    global playersStatus
    global GAME_NUMBER_OF_PLAYERS
    global ADDR
    global restartFlag


    if(restartFlag):
        os.execv(sys.argv[0], sys.argv);

    print("[STARTING] SURVIBALL server starting...")
    param_IP = sys.argv[1]
    param_PORT = int(sys.argv[2])     
    param_players = int(sys.argv[3])

    IP = param_IP;
    PORT = param_PORT;
    GAME_NUMBER_OF_PLAYERS = param_players;
    ADDR = (IP, PORT)

    print(f"[STATUS] Server address {param_IP}")
    print(f"[STATUS] Server port {param_PORT}")
    print(f"[STATUS] Game number of players {param_players}")


    try:    
        server.shutdown(socket.SHUT_RDWR)
    except: 
        pass;

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    server.bind(ADDR)
    server.listen()

    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    
    randomSeedGenerated = random.randint(1,100);
    playersStatus["sys_randomSeed"] = randomSeedGenerated;

    print(f"[STATUS] Ball seed generated {randomSeedGenerated}")
    #generatePlayerHashes();

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
    print("[STATUS] All threads finished");
    #os.execv(sys.argv[0], sys.argv)

if __name__ == "__main__":
    main()