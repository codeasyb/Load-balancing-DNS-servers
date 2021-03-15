import socket, sys
import time, random
def localhost():
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if ls is ls:
        print("[LS]: Socket created")
    else:
        print("[LS]: Error creating socket")
        exit()

    ls_address = ('', lsListenPort)
    ls.bind(ls_address)
    ls.listen(1)
    print("[LS]: listening on port: {}".format(lsListenPort))

    while True:
        ls_conn, ls_addr = ls.accept()
        client_query = "!empty" 
        
        while client_query != "":
            client_query = ls_conn.recv(200).decode("utf-8")
            time.sleep(random.random()*5)
            print("[C]: looking for {}".format(client_query))
            
            # Ts1 behavior
            ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[Ts1]: Socket Created")
                    
            ts1_ip = socket.gethostbyname(ts1Hostname)
            ts1_addr = (ts1Hostname, ts1ListenPort)
            print("[Ts1]: [{}] listening on {}".format(ts1Hostname, ts1ListenPort))
            ts1.connect(ts1_addr)
                
            ts1.send(client_query.encode("utf-8"))                         
            print("[Ts1]: finding => {}".format(client_query))
            ts1_response = ts1.recv(200).decode("utf-8")                    
            ts1_response_check = ts1_response.split()
            # print("==> {}".format(ts1_response_check))

            ts1Sent = 0;
            ts2Sent = 0;
            print(len(ts1_response_check))
            if len(ts1_response_check) == 5:
                print("TS1 Not found")
                # Ts2 Behavior
                ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[Ts2]: Socket Created")
                        
                ts2_ip = socket.gethostbyname(ts2Hostname)
                ts2_addr = (ts2Hostname, ts2ListenPort)                
                ts2.connect(ts2_addr)
                print("[Ts2]: [{}] listening on {}".format(ts2Hostname, ts2ListenPort))
                    
                ts2.send(client_query.encode("utf-8"))                          
                print("[Ts2]: finding => {}".format(client_query))
                # print("[Ts2]: {}".format(client_query))
                ts2_response = ts2.recv(200).decode("utf-8")                    
                ts2_response_check = ts2_response.split()
                # print("==> {}".format(ts2_response_check))
                if len(ts2_response_check) == 5: 
                    print("TS2 Not found")                              
                else: 
                    ls_conn.send(ts2_response.encode("utf-8"))
                    ts2Sent = 1
            else: 
                ls_conn.send(ts1_response.encode("utf-8"))                  
                ts1Sent = 1
            
            if not (ts1Sent or ts2Sent):
                ls_conn.send(".".encode("utf-8"))
        ts1.close()
        ts2.close()                    
    ls.close()

            
if __name__ == "__main__":
    lsListenPort = int(sys.argv[1])
    ts1Hostname = sys.argv[2]
    ts1ListenPort = int(sys.argv[3])
    ts2Hostname = sys.argv[4]
    ts2ListenPort = int(sys.argv[5])
    localhost()