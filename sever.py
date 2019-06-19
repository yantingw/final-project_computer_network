import socket,threading
import cv2
import numpy
import pickle
import sys
import pyaudio
import time
TCP_IP = '192.168.2.42'


def check_ip(ipAd):
    try :
        with open('pickle_example.pickle', 'rb') as file:
            ipdict = pickle.load(file)
            
        if ipAd in ipdict.keys():
            ipdict[ipAd]+=1
            print(f"check ip number :{ipdict}")
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

    return ipdict[ipAd] > 100
def refresh_record():
    while true:
        try :
            with open('pickle_example.pickle', 'rb') as file: 
                ipdict = pickle.load(file)    
                for ipAd in ipdict.keys():
                    ipdict[ipAd]=0    

            with open('pickle_example.pickle', 'wb') as file:
                    pickle.dump(ipdict, file)
                    file.close()    
        time.sleep( 5*60 )

    

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
def open_new_socket(conn,addr,num_of_client):
    
    TCP_PORT = 6000+(num_of_client)
    new_port =str(TCP_PORT) 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    print(TCP_PORT)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)
    conn.send(new_port.encode()) #send the new port 
    conn, addr = s.accept()
    print("complete!!!")
    return conn,addr


def serve_the_client(conn,addr,num_of_client):
    
    if check_ip(addr[0]):
        conn.send("request too frequent".encode())    
        conn.shutdown(socket.SHUT_RDWR)
        sys.exit("some error message")#can be removed
    else:
        conn,addr = open_new_socket(conn,addr,num_of_client) 
        strea = recor()
        print(f"the client addr is {addr}")
        conn.send("start".encode())
        ret, frame = capture.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
        current_pixel=720
        estimated_rtt=0
        alpha=0.125
        while ret:
            if current_pixel == 480:
                frame=cv2.resize(frame, (60,40))
    #            print(f"send the diffrent img :   {frame.shape}")

            if conn.recv(5).decode() == "start":
                sendt = time.time()
            conn.send(strea.read(2048))
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
     #       print(f"send orgin img :   {imgencode.shape}")           
            data = numpy.array(imgencode)
            stringData = data.tostring() 
            
                
            conn.send(str(len(stringData)).ljust(16).encode())
            
            conn.send(stringData)
            

                        

            #"""cv2.imshow('SERVER2',decimg)"""
            mess= conn.recv(3).decode()
            if mess == "ok!":
                rtt_t = time.time() - sendt
                if estimated_rtt == 0:
                    estimated_rtt=rtt_t
                estimated_rtt=(1-alpha)*estimated_rtt + alpha*rtt_t
                cv2.waitKey(int(estimated_rtt*1000))
                if estimated_rtt > 0.05 :
                    x = int(1080*10/(estimated_rtt*1000))
                    y = int(760*10/(estimated_rtt*1000))
                else :
                    x = 1080
                    y = 760

                print('RTT time: {} ms'.format(int(estimated_rtt*1000)), end="\r")
            else:
                
                if mess == "480":
                    current_pixel=480
                    print('改變pixel480')
                elif mess == "720":
                    current_pixel=720
                    print('改變pixel720')
                
                cv2.waitKey(100)
            ret, frame = capture.read()
            frame=cv2.resize(frame, (x,y))
            print(f"now frame size is {frame.size}.")
      #      print(ret)

        conn.close()
        cv2.destroyAllWindows()



        
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
#def main(): 

capture = cv2.VideoCapture(0)
chc = int(input("輸入希望像素(如 480, 720):"))
num_of_client = 0
if chc == 480:
    make_480p()
else:
    make_720p()
threading.Thread(target = refresh_record,name= 'thread-refresh_record').start()    
TCP_PORT = 6000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind((TCP_IP, TCP_PORT))
while(True):
    s.listen(True)
    #get a client    
    conn, addr = s.accept()
    print(conn,addr)
    num_of_client+=1
    threading.Thread(target = serve_the_client,args =(conn,addr,num_of_client),name= 'thread-'+str(num_of_client)).start()    
    
    print("finish threads: %s",num_of_client)
