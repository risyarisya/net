import numpy as np
from PIL import Image
import socket
import struct
import binascii
import imgproc

def receiveRawImg(conn, length, width, height):
    bufs = []
    bytes_recved = 0
    while bytes_recved < length:
        buf = conn.recv(min(length-bytes_recved, 2048))
        bufs.append(buf)
        bytes_recved += len(buf)
    return b''.join(bufs)

def sendCMYKData(conn, data):
    cmyk = data.convert('CMYK')
    splited = cmyk.split()
    for ch in splited:
        tmp = np.asarray(ch)
        width, height = tmp.shape
        msglen = width*height
        msg = tmp.tobytes()
        totalsent = 0
        
        while totalsent < msglen:
            sent = conn.send(msg[totalsent:])
            totalsent += sent
            print(totalesnt)


def main():
    host = '127.0.0.1'
    port = 12345
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((host, port))
    sock.listen(10)
    headerUnpacker = struct.Struct('B L L L')
    while True:
        conn, address = sock.accept()
        buf = conn.recv(headerUnpacker.size)
        print("%s"%binascii.hexlify(buf))
        id, len, imgWidth, imgHeight = headerUnpacker.unpack(buf)
        print("id=%d, len=%d, imgWidth=%d, imgHeight=%d"%(id, len, imgWidth, imgHeight))
        data = receiveRawImg(conn, imgWidth*imgHeight*3, imgWidth, imgHeight)

        # send Ack
        senddata = struct.pack("BL", 1, 0)
        conn.send(senddata)

        dataarray = np.fromstring(data, dtype=np.uint8)
        print(dataarray.shape)
        dataarray.shape = (imgHeight, imgWidth, 3)
        imgdata = Image.fromarray(dataarray)
#        imgdata.save('recv.jpg', 'JPEG')
        cmykimg = imgdata.convert('CMYK').split()
        chnum = 1
        for ch in cmykimg:
            tmp = np.asarray(ch, dtype=np.uint8)
            conn.send(struct.pack("BL", chnum, tmp.size))
            bi = tmp.tobytes()
            totalsent = 0
            chnum += 1
            while totalsent < tmp.size:
                sent = conn.send(bi[totalsent:])
                totalsent += sent
                print("sent=%d"%totalsent)
        break;

main()
