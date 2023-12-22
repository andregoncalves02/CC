import pickle
import sys
import threading
import time
from leitor import*
from message import message
from newcache import cache
import socket 
import struct
from logs import*

class SS:
    #achamos que na inicialização era importante obter logo os dados do ficheiro config 
    def __init__(self,name):
        self.name=name
        self.cache = cache()
        self.ficheiro_db = None
        self.fichero_log = None
        self.fichero_log_all = None
        self.lista_sts = []
        self.ipSP = None
        self.dd = None
        leitor_file("config", "/home/core/Desktop/Trabalho/file_" + name + "/config_" + name + "_ss.txt",self)
        logsEV("conf-file-read","/home/core/Desktop/Trabalho/file_" + name + "/config_" + name + "_ss.txt",self.getlogs(),self.getalllogs())
    
    def getName(self):
        return self.name

    def setFileDB(self, fileDB):
        self.ficheiro_db=fileDB

    def setipSP(self, ip):
        self.ipSP = ip

    def getipSP(self):
        return self.ipSP
    
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

    def getCache(self):
        return self.cache
    
    def addto_cache(self,line,org,default):
        self.cache.add_line(line,org,default)

    def bd_valida(self):
        self.cache.bd_valida(self.name)

    #o servidor cria um socket tcp e tenta comunicar se com SP-> envia uma mensagem com o dominio que pretende -> recebe o numero de linhas de informaçao-> responde ok->começa a receber a informaçao e a guarda la na cache 
    def pedeTransferencia(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.getipSP(),1060))
        msg = "domain: "+ self.getName()
        s.send(msg.encode('utf-8'))
        newmsg =s.recv(1024).decode('utf-8')
        msg = "ok"
        s.send(msg.encode('utf-8'))
        msgs=newmsg.split()
        if(len(msgs)>1):
            num = int(msgs[1])
            i=0
            alllines = []
            while i !=num:
                newmsg=s.recv(1024).decode('utf-8')
                lines = newmsg.split("\n")
                for line in lines:
                    a = line.split(":")[0]
                    if a != "":
                        i=int(a)
                        alllines.append(line)
            leitor_cache_line(alllines,self,"TZ")        
            logZT("SS",str(self.getipSP()),self.getlogs(),self.getalllogs())
        else:
            logEZ("SP",str(self.getipSP()),self.getlogs(),self.getalllogs())
        s.close()

    #esta funçao recebe a querry escreve a nos logs e pergunta a cache pela resposta depois escreva na querry
    def responde(self,dnsmsg,add,s):
        dnsmsg =  pickle.loads(dnsmsg)
        queryRE("QR",str(add[0]),self.getlogs(),self.getalllogs())

        name=dnsmsg.getQname()
        type=dnsmsg.getQtype()
  
        if name == self.name.replace("_",".") +".":
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
            ip = self.cache.procura_sv(dnsmsg.getQname())
            news = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            queryRE("QE",str(ip),self.getlogs(),self.getalllogs())
            news.sendto(dnsmsg.to_bytes(), (ip, 1050))
            msg, add1 = news.recvfrom(1024)
            queryRE("QR",str(ip),self.getlogs(),self.getalllogs())
            msg=pickle.loads(msg)

            if msg.getResponse_values() == None:
                msg.setResponseCode("2")

            return s.sendto(msg.to_bytes(), add)
        else:
            ip = self.cache.procura_sv(dnsmsg.getQname())
            return s.sendto(str(ip).encode('utf-8'), add)
        queryRE("QE",str(add[0]),self.getlogs(),self.getalllogs())
        s.sendto(dnsmsg.to_bytes(), add)

def cliente(Sss,endereco):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    porta = 1050
    s.bind((endereco, porta ))

    while True:
        (msg, add) = s.recvfrom(1024)

        threading.Thread(target=Sss.responde, args=(msg,add,s,)).start()

def TZ(Sss):
    while True:
        if(Sss.bd_valida()):
            Sss.pedeTransferencia()
        time.sleep(1)



#logo apos o servidor ser inicializado peddimos uma transferencia de zona para reter alguma coisa na cache
#a comunicaçao com cliente vai ser sempre feita na porta 1050 com um socket udp
# o servidor espera por uma mensagem do cliente ->quando recebe respondde internamente e ddepois envia de volta ao cliente
def main():
    if len(sys.argv)>2:
        Sss = SS(sys.argv[1])

        Sss.pedeTransferencia()

        threading.Thread(target=cliente,args=(Sss,sys.argv[2])).start()
        threading.Thread(target=TZ,args=(Sss,)).start()

    else:
        print("error in args")

main()