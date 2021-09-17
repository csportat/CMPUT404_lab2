#!/usr/bin/env python3
import socket, time, sys

# Define global address and buffer size 
HOST = ""
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

def main():
    # Address for Step 6-8 
    extern_host = 'www.google.com'
    extern_host_alias = 'Google'
    extern_port = 80
    
    # Create socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server...')
        
        # Allow reused addresses, bind the socket, and set to listening mode 
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind( (HOST, PORT) )
        proxy_start.listen(1)
        
        while True:
            # Connect proxy_start 
            conn, addr = proxy_start.accept()
            print('Connected by', addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print(f'Connecting to {extern_host_alias}...')
                remote_ip = get_remote_ip(extern_host)
                
                # Connect proxy_end 
                proxy_end.connect( (remote_ip, extern_port) )
                
                # Send data 
                send_full_data = conn.recv(BUFFER_SIZE)
                print(f'Sending received data {send_full_data} to {extern_host_alias}...')
                proxy_end.sendall(send_full_data)
                
                # Shut down 
                proxy_end.shutdown(socket.SHUT_WR)
                
                data = proxy_end.recv(BUFFER_SIZE)
                print(f'Sending received data {data} to client...')
                # Send data back 
                conn.send(data)
                
            conn.close()
        
if __name__ == "__main__":
    main()
