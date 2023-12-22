import socket
import sys
from message import message

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = message("")
if len(sys.argv)>2:
    ip_address= sys.argv[1]
    msg.setQname(sys.argv[2])
    msg.setQtype(sys.argv[3])
    if len(sys.argv)==5:
        msg.setflags(sys.argv[4])
    s.sendto(msg.to_string().encode('utf-8'), (ip_address, 1050))
    new_msg, add = s.recvfrom(1024)
    print(f"Recebi uma mensagem do servidor {add}")
    print(new_msg.decode('utf-8'))
else:
    print("error")

