import pickle
from message import message
from newcache import cache
from leitor import*
from logs import*
import socket
import time
import threading
import sys

class Sr:
    def __init__(self, name):
        self.name=name
        self.dns_domain=None
        self.ficheiroLog=None
        self.fichero_log_all = None
        self.top_servers=[]
        leitor_file("config", "/home/core/Desktop/Trabalho/file_SR/config_sr.txt", self)
        logsEV("conf-file-read", "/home/core/Desktop/Trabalho/file_SR/config_sr.txt",self.getlogs(), self.getalllogs())

    def setDD(self, ip):
        self.dns_domain=ip
    def setlogs(self, file):
        self.ficheiroLog=file
    def getlogs(self):
        return self.ficheiroLog
    def setalllogs(self, file):
        self.fichero_log_all=file
    def getalllogs(self):
        return self.fichero_log_all
    def setlistaSTS(self, ip):
        self.top_servers = ip

    def pergunta(self, dnsmsg, ipC, s):
        dnsmsg=pickle.loads(dnsmsg)

        name = dnsmsg.getQname()
        aux = 0
        flags=dnsmsg.getflags()
        while(name):
            if(name==self.name):
                aux=1
                break
            else:
                while name:
                    for l in name:
                        if l == ".":
                            name = name.replace(l, "", 1)
                            break
                        name = name.replace(l, "", 1)
        news = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if "R" in flags:
            if aux==1:

                news.sendto(dnsmsg.to_bytes(), (self.dns_domain, 1050))
                queryRE("QE", self.dns_domain, self.ficheiroLog, self.fichero_log_all)
            else:
                news.sendto(dnsmsg.to_bytes(), (self.top_servers[0], 1050))
                queryRE("QE", self.top_servers[0], self.ficheiroLog, self.fichero_log_all)
            (msg, add) = news.recvfrom(1024)
            queryRE("QR", str(add[0]), self.ficheiroLog, self.fichero_log_all)
            s.sendto(msg,ipC)
            queryRE("QE", str(ipC[0]), self.ficheiroLog, self.fichero_log_all)
        else:
            if aux == 1:
                news.sendto(dnsmsg.to_bytes(), (self.dns_domain, 1050))
                queryRE("QE", self.dns_domain, self.ficheiroLog, self.fichero_log_all)
            else:
                news.sendto(dnsmsg.to_bytes(), (self.top_servers[0], 1050))
                queryRE("QE", self.top_servers[0], self.ficheiroLog, self.fichero_log_all)

            (msg, add) = news.recvfrom(1024)
            queryRE("QR", str(add[0]), self.ficheiroLog, self.fichero_log_all)
            while type (pickle.loads(msg)) is str:
                news.sendto(dnsmsg.to_bytes(), (pickle.loads(msg), 1050))
                queryRE("QE", pickle.loads(msg), self.ficheiroLog, self.fichero_log_all)
                (msg, add) = news.recvfrom(1024)
            queryRE("QR", str(add[0]), self.ficheiroLog, self.fichero_log_all)
            s.sendto(msg, ipC)
            queryRE("QE", str(ipC[0]), self.ficheiroLog, self.fichero_log_all)







def cliente(Sr, endereco):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            porta = 1050
            s.bind((endereco, porta))

            while True:
                (msg, add) = s.recvfrom(1024)

                threading.Thread(target=Sr.pergunta, args=(msg, add, s,)).start()

def main():
    if len(sys.argv) > 2:
        Srr = Sr(sys.argv[1])


        cliente(Srr, sys.argv[2])

    else:
        print("error with name")


main()