import socket
import cv2
import numpy
import sys
import keyboard
import pyaudio

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
RECORD_SECONDS = 0.015

TCP_IP = '10.129.207.29'
#TCP_IP = 'localhost'
TCP_PORT = 6000



sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
print("connect build!!!")
new_port =int( sock.recv(50).decode())
print(new_port)
#build a new connection
sock.close()
sock = socket.socket()
sock.connect((TCP_IP, new_port))

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)



dat = sock.recv(50).decode()


#try:
while 1:
    sock.send("start".encode())
    stream.write(sock.recv(4096))
    length = recvall(sock,16)
    stringData = recvall(sock, int(length)) 
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)###dat
    decimg =cv2.resize(decimg,(1080,720))
    cv2.imshow("vedio",decimg)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
    #if keyboard.is_pressed('space'):
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.destroyAllWindows()
        #mess = raw_input("輸入欲更改的像素:")
        mess =input("輸入欲更改像素(如 480, 720):")
        sock.send(mess.encode())    
    else:
        sock.send("ok!".encode())

#except Exception:
#   sys.exit(dat)

sock.close()
cv2.destroyAllWindows()
