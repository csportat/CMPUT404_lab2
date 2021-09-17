#!/usr/bin/env python3
import socket, time
from multiprocessing import Process

# Define global address and buffer size 
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# Echo connections back to client 
def handle_echo(addr, conn):
    print('Connected by', addr)
    
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
    # Create socket, allow reused addresses, bind the socket, and set to listening mode 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind( (HOST, PORT) )
        s.listen(2)
        
        while True:
            # Accept connections and start a process daemon for handling multiple connections 
            conn, addr = s.accept()
            p = Process( target=handle_echo, args=(addr, conn) )
            p.daemon = True
            p.start()
            print('Process started ', p)
            
if __name__ == "__main__":
    main()
