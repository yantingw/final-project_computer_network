import socket
import  threading


def open_new_socket(self,conn,addr):
        
    TCP_IP = 'localhost'
    self.TCP_PORT += 1 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)

