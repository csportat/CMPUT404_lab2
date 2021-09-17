#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

# Define global address and buffer size 
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

# Get IP 
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting...')
        sys.exit()
    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

# Handle request from client 
def handle_request(conn, addr, proxy_end):
    client_full_data = conn.recv(BUFFER_SIZE)
    print(f'Sending received data {client_full_data} to external host (Google)...')
    proxy_end.sendall(client_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    
    external_full_data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {external_full_data} to client...')
    conn.sendall(external_full_data)
    conn.shutdown(socket.SHUT_RDWR)
    
    return

def main():
    extern_host = 'www.google.com'
    extern_host_alias = 'Google'
    extern_port = 80
    
    # Create "start" socket of proxy which connects to localhost 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server...')
        
        # Allow reused addresses, bind the socket, and set to listening mode 
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind( (HOST, PORT) )
        proxy_start.listen(2)
        
        while True:
            # Accept incoming connections from proxy_start 
            conn, addr = proxy_start.accept()
            print('Connected by', addr)
            
            # Create "end" socket of proxy which connects to external host 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print(f'Connecting to {extern_host_alias}...')
                remote_ip = get_remote_ip(extern_host)
                # Connect proxy_end to remote IP of external host 
                proxy_end.connect( (remote_ip, extern_port) )
                
                p = Process( target=handle_request, args=(conn, addr, proxy_end) )
                p.daemon = True
                p.start()
                print('Process started ', p)
                
            conn.close()
                
if __name__ == "__main__":
    main()