from message import message
from newcache import cache
from leitor import*
from logs import*
import socket 
import time
import threading
import sys

class Sp:
    #achamos que na inicialização era importante obter logo os dados do ficheiro config e da base de dados
    def __init__(self,name):
        self.name=name
        self.cache = cache()
        self.ficheiro_db = None
        self.fichero_log = None
        self.fichero_log_all = None
        self.lista_sts = []
        self.ipSS = []
        self.dd = None
        leitor_file("config", "/home/core/Desktop/Trabalho/file_" + name + "/config_" + name + "_sp.txt",self)
        leitor_cache("/home/core/Desktop/Trabalho/file_" + name + "/cache_" + name + ".db",self,"FILE")
        logsEV("conf-file-read","/home/core/Desktop/Trabalho/file_" + name + "/config_" + name + "_sp.txt",self.getlogs(),self.getalllogs())
        logsEV("bd-file-read","/home/core/Desktop/Trabalho/file_" + name + "/cache_" + name + ".db",self.getlogs(),self.getalllogs())
    
    def setFileDB(self, fileDB):
        self.ficheiro_db=fileDB

    def getFileDB(self):
        return self.ficheiro_db

    def setipSS(self, ip):
        self.ipSS.append(ip)
    
    def setDD(self, dd):
        self.dd=dd
    
    def setlistaSTS(self, sts):
        self.lista_sts.append(sts)
    
    def setlogs(self, logs):
        self.fichero_log = logs

    def getlogs(self):
        return self.fichero_log

    def setalllogs(self, logs):
        self.fichero_log_all = logs
    
    def getalllogs(self):
        return self.fichero_log_all

    def setCache(self, cache):
        self.cache=cache

    def addto_cache(self,line,org,default):
        self.cache.add_line(line,org,default)
    
    #esta funçao recebe a querry escreve a nos logs e pergunta a cache pela resposta depois escreva na querry
    def responde(self,dnsmsg,add,s):
        print(dnsmsg.decode('utf-8'))
        print(f"Recebi uma mensagem do cliente {add}")
        queryRE("QR",str(add[0]),self.getlogs(),self.getalllogs())

        dnsmsg = message(dnsmsg.decode('utf-8'))
        name=dnsmsg.getQname()
        type=dnsmsg.getQtype()
        if dnsmsg.getQtype() == "PTR" and  self.name == "reverse":
            hostname = self.cache.procura_reverse(dnsmsg.getQname())
            if hostname is not None:
                response = [hostname+" PTR "+name]
                dnsmsg.setn_values(len(response))
                dnsmsg.setResponse_values(response)
                dnsmsg.setn_authority(0)
                dnsmsg.setn_extravalues(0)
                flags = dnsmsg.getflags().replace("Q+", "").replace("A+", "").replace("Q", "").replace("A", "") + "+A"
                dnsmsg.setflags(flags)
            else:
                dnsmsg.setResponseCode("3")
        elif name == self.name.replace("_",".")  +".":
            response,authority,extra =self.cache.procura(name,type)
            if len(response)>0:
                dnsmsg.setn_values(len(response))
                dnsmsg.setResponse_values(response)
                dnsmsg.setn_authority(len(authority))
                dnsmsg.setAutority_values(authority)
                dnsmsg.setn_extravalues(len(extra))
                dnsmsg.setExtra_values(extra)
                flags=dnsmsg.getflags().replace("Q+","").replace("A+","").replace("Q","").replace("A","")+"+A"
                dnsmsg.setflags(flags)
            else:
                dnsmsg.setResponseCode("1")
        elif "R" in dnsmsg.getflags():
            if dnsmsg.getQtype() == "PTR":
                name = "reverse."
            ip = self.cache.procura_sv(name)
            print(ip)
            news = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            queryRE("QE",str(ip),self.getlogs(),self.getalllogs())
            news.sendto(dnsmsg.to_string().encode('utf-8'), (ip, 1050))
            msg, add1 = news.recvfrom(1024)
            msg=msg.decode('utf-8')
            print(msg)
            print(f"Recebi uma mensagem do servidor {add}")
            queryRE("QR",str(ip),self.getlogs(),self.getalllogs())

            newmsg = message(msg)
            if newmsg.getResponse_values() == None:
                newmsg.setResponseCode("2")
            print(newmsg.to_string())
            print(f"Enviei uma mensagem para o servidor {add}")
            queryRE("QE",str(add[0]),self.getlogs(),self.getalllogs())
            return s.sendto(newmsg.to_string().encode('utf-8'), add)
        else:
            if dnsmsg.getQtype() == "PTR":
                name = "reverse."
            ip = self.cache.procura_sv(name)
            return s.sendto(str(ip).encode('utf-8'), add)

        print(dnsmsg.to_string())
        print(f"Enviei uma mensagem para o servidor {add}")
        queryRE("QE",str(add[0]),self.getlogs(),self.getalllogs())
        s.sendto(dnsmsg.to_string().encode('utf-8'), add)


#a comunicaçao com cliente vai ser sempre feita na porta 1050 com um socket udp
# o servidor espera por uma mensagem do cliente ->quando recebe respondde internamente e ddepois envia de volta ao cliente
def cliente(Spp,endereco):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    porta = 1050
    s.bind((endereco, porta ))

    print(f"Estou à escuta no {endereco}:{porta}")
    while True:
        (msg, add) = s.recvfrom(1024)

        threading.Thread(target=Spp.responde, args=(msg,add,s,)).start()


#a traznferencia de zona vai ter um socket tcp em especifico e tera sempre a porta 1060 como predefenida
#o servidor ira receber uma mensagem com o dominio que é pedido -> envia uma mensagem com o numero de linhas que ira enviar -> recebe um ok -> envia a informaçao linha a linha
#temos um sleep pois se nao as informaçoes acomulan se na connection e o SS ira ler varias linhas ao mesmo tempo
def TTZ(Spp,endereco):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    porta = 1060
    s.bind((endereco, porta ))
    s.listen()

    while True:
        connection, add = s.accept()
        threading.Thread(target=TZ, args=(Spp,connection,add,)).start()
        

def TZ(Spp,connection,add):
    msg = connection.recv(1024).decode('utf-8')
    msgs=msg.split()
    if(len(msgs)>1):
        if(msgs[1]==Spp.name):
            f=open(Spp.getFileDB())
            counter=0
            lines=[]
            for line in f:
                if line[0]!='#' and line[0]!='\n':
                    counter+=1
                    lines.append(str(counter)+": "+line +"\n")
            newmsg="entries: " + str(counter)
            connection.sendto(newmsg.encode('utf-8'), add)
            msg = connection.recv(1024).decode('utf-8')
            if(msg=="ok"):
                for line in lines:
                    connection.sendto(line.encode('utf-8'), add)
                connection.close()
                logZT("Sp",str(add),Spp.getlogs(),Spp.getalllogs())
            else:
                connection.close()
                logEZ("SP",str(add),Spp.getlogs(),Spp.getalllogs())
        else:
            connection.close()
            logEZ("SP",str(add),Spp.getlogs(),Spp.getalllogs())
    else:
        connection.close()
        logEZ("SP",str(add),Spp.getlogs(),Spp.getalllogs())


#existem duas threads uma para tratar dos clientes e uma para tratar dos pedidos de transferencia de zona
def main():
    if len(sys.argv)>2:
        Spp = Sp(sys.argv[1])

        print(Spp.getFileDB())
        threading.Thread(target=cliente,args=(Spp,sys.argv[2])).start()
        threading.Thread(target=TTZ,args=(Spp,sys.argv[2])).start()
    else:
        print("error with name")

main()