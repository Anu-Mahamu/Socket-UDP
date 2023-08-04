'''This is the server code to send video frames over UDP
    Essential modules are imported'''
#cv2 module for real-time computer vision
import cv2
import imutils
import socket
import numpy as np
import time
from tkinter import *
from threading import *
#we use base64 to convert the image data into text format and vise versa
import base64
def server(tab):
    BUFF_SIZE=65536
    #UDP server socket is created
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_name=socket.gethostname()
    #Let's get the host IP address
    host_ip=socket.gethostbyname(host_name)
    Label(tab,text=host_ip,bg="black",fg="white").pack()
    print(host_ip)
    port=56519
    #with the port and IP we will make the socket address
    socket_address=(host_ip,port)
    server_socket.bind(socket_address)
    print('Listening at:',socket_address)
    a='Listening at:'+str(socket_address)
    Label(tab,text=a,bg="black",fg="white").pack()
    #we mention a mp4 file already we have
    vid=cv2.VideoCapture('Sastra.mp4')
    #Initialising variables to obtain frame rate
    fps,st,frames_to_count,cnt=(0,0,100,0)
    #In this loop the server will try to receive datagram from any client 
    while True:
        msg,client_addr=server_socket.recvfrom(BUFF_SIZE)
        print('got connection from',client_addr)
        WIDTH=400
        while(vid.isOpened()):
            _,frame=vid.read()
            frame=imutils.resize(frame,width=WIDTH)
            encoded,buffer=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message=base64.b64encode(buffer)
    #sending this message to the client address
            server_socket.sendto(message,client_addr)
            frame=cv2.putText(frame,'FPS:'+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,200),2)
    #imshow function is used to display the transmitted frame at the server
            cv2.imshow('TRANSMITTING VIDEO',frame)
            key=cv2.waitKey(1)&0xFF
            if key==ord('q'):
                server_socket.close()
                break
    #using this frames to calculate frames per second
            if cnt==frames_to_count:
                try:
                    fps=round(frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1
def send():
    b1.destroy()
    t1=Thread(target=server,args=(tab,))
    t1.start()
tab=Tk()
tab.geometry("200x200")
tab.config(bg="lightgray")
b1=Button(tab,text="start streaming",command=send,bg="black",fg="white")
b1.place(x=60,y=75)
tab.mainloop()
