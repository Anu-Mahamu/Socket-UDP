#This is the client code to receive video frames over UDP
#Essential modules are imported
import cv2
#This is the client code to receive video frames over UDP
#Essential modules are imported
import imutils
import socket
import numpy as np
import time
#we use base64 to convert the image data into text format and vice versa
import base64
BUFF_SIZE=65536
#UDP client socket is created
client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name=socket.gethostname()
#socket ip address and port number is given
host_ip='192.168.43.10'
print(host_ip)
port=56519
#here hello datagram is sent to server
message=b'hello'
client_socket.sendto(message,(host_ip,port))
#variables are initialised to obtain the frame rate
fps,st,frames_to_count,cnt=(0,0,20,0)
#receiving the data using the while loop
while True:
    packet,_=client_socket.recvfrom(BUFF_SIZE)
#the received data is decoded
    data=base64.b64decode(packet,' /')
    npdata=np.frombuffer(data,dtype=np.uint8)
    frame=cv2.imdecode(npdata,1)
    frame=cv2.putText(frame,'FPS:'+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
#imshow function is used to display the received frame at client side from server
    cv2.imshow("RECIVING VIDEO",frame)
    key=cv2.waitKey(1)&0xFF
    if key==ord('q'):
                client_socket.close()
                break
#using this frames to calculate frames per second
    if cnt==frames_to_count:
            try:
                fps=round(frames_to_count/(time.time()-st))
                st.time.time()
                cnt=0
            except:
                pass
    cnt+=1 
