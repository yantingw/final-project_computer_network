import socket
import cv2
import numpy
import sys
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

#TCP_IP = '192.168.2.42'
TCP_IP = 'localhost'
TCP_PORT = 6000



sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
new_port = sock.recv(50).decode()
print(new_port)

'''
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)



dat = sock.recv(50).decode()



print (f"get!!! {dat}")


try:
    while 1:
        sock.send("start".encode())
        stream.write(sock.recv(4096))
        length = recvall(sock,16)
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        cv2.imshow('CLIENT2',decimg)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        sock.send("ok".encode())
except Exception:
    sys.exit(dat)

sock.close()
cv2.destroyAllWindows()
'''
