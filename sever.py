import socket
import cv2
import numpy
import pickle
import sys
import pyaudio
import time
def check_ip(ipAd):
    try :
        with open('pickle_example.pickle', 'rb') as file:
            ipdict = pickle.load(file)    
        if ipAd in ipdict.keys():
            ipdict[ipAd]+=1    
        else:
            ipdict[ipAd] = 0

        with open('pickle_example.pickle', 'wb') as file:
            pickle.dump(ipdict, file)
            print(ipdict)
    except :   
        with open('pickle_example.pickle', 'wb') as file:
            ipdict = {}
            ipdict[ipAd] = 0
            print(ipdict)
            pickle.dump(ipdict,file)
            print("make the pickle file")

    return ipdict[ipAd] > 4000000000


def callback(in_data, frame_count, time_info, status):
    conn.send(in_data)   

    return (None, pyaudio.paContinue)
def recor():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024  
    stream = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS,

                    rate=RATE, input=True,

                    frames_per_buffer=CHUNK)
    print("recording...")
    

    return stream
        


 


def make_1080p():
    capture.set(3, 1920)
    capture.set(4, 1080)

def make_720p():
    capture.set(3, 1280)
    capture.set(4, 720)

def make_480p():
    capture.set(3, 640)
    capture.set(4, 480)

capture = cv2.VideoCapture(0)
chc = int(input("輸入希望像素(如 480, 720):"))

if chc == 480:
    make_480p()
else:
    make_720p()

TCP_IP = 'localhost'
TCP_PORT = 6000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
    

ret, frame = capture.read()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]


conn, addr = s.accept()

if check_ip(addr[0]):
    conn.send("request too frequent".encode())    
    conn.shutdown(socket.SHUT_RDWR)
    sys.exit("some error message")
strea = recor()
print(f"the ret is {ret}")
print(addr)
conn.send("start".encode())
while ret:
    if conn.recv(5).decode() == "start":
        sendt = time.time()
    conn.send(strea.read(2048))
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring() 
      
    conn.send(str(len(stringData)).ljust(16).encode())
    
    conn.send(stringData)
    
    #decimg = cv2.imdecode(data,1)
    

    #"""cv2.imshow('SERVER2',decimg)"""
    
    if conn.recv(2).decode() == "ok":
        rtt_t = time.time() - sendt
        print('RTT time: {} seconds'.format(rtt_t), end="\r")
    
    cv2.waitKey(20)
    ret, frame = capture.read()

#conn.close()
cv2.destroyAllWindows()