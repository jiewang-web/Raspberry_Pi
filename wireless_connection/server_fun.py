#! /usr/bin/env python

import socket
import time
 
def socket_receive():
    TCP_IP = '172.25.111.204' # '192.168.1.17'#'172.27.41.41'
    TCP_PORT = 6677
    BUFFER_SIZE = 800  # Normally 1024, but we want fast response
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)

    while  True:
        try:
            conn, addr = s.accept()
            print ('Connection address:', addr)
            conn.settimeout(30)
            
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            print ("received data:", data)
            conn.send(data)  # echo
            return data
        except s.timeout:  
            print ('time out')
            break
    conn.close()
    s.close()                  

