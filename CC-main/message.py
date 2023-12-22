import pickle
import random

#esta classe serve para que o servidor consiga aceder rapidamente a informaçao que precisa da querry e tambem para alterala 
#por tanro é bastante importante conseguir atraves de uma string criar um objeto desta classe e vice-versa
class message:

    def __init__(self,msg):
        parte = msg.split(";")
        if(len(parte)>1):
            parte1 = parte[0].split(',')
            if(len(parte1)>5):
                self.id=parte1[0]
                self.flags=parte1[1]
                self.reponsecode=parte1[2]
                self.n_values=parte1[3]
                self.n_autority=parte1[4]
                self.extra_values=parte1[5]
            parte2 = parte[1].split(',')
            if(len(parte2)>1):
                self.Q_name=parte2[0]
                self.type=parte2[1] 
        else:
            self.id=random.randint(1,65535)
            self.flags=[]
            self.reponsecode=0
            self.n_values=0
            self.n_autority=0
            self.extra_values=0
            self.Q_name=""
            self.type=""
            self.Response_values=[]
            self.Autority_values=[]
            self.Extra_values=[]

        if(len(parte)>4):
            self.Response_values=parte[2].split(",")
            self.Autority_values=parte[3].split(",")
            self.Extra_values=parte[4].split(",")
        elif(len(parte)>3):
            self.Response_values=parte[2].split(",")
            self.Autority_values=parte[3].split(",")
            self.Extra_values=[]
        elif(len(parte)>2):
            self.Response_values=parte[2].split("")
            self.Autority_values=[]
            self.Extra_values=[]
        else:
            self.Response_values=[]
            self.Autority_values=[]
            self.Extra_values=[]

    def to_string(self):
        cabeçalho =str(self.id)+','+ str(self.flags) +','+ str(self.reponsecode) + ','+str(self.n_values) +','+ str(self.n_autority) +','+ str(self.extra_values) +';'+ str(self.Q_name) +','+ str(self.type) +';'
        listas=""
        for i in self.Response_values:
            listas = listas + str(i) + ","
        listas = listas[:-1]
        listas = listas + ";"
        for i in self.Autority_values:
            listas = listas + str(i) + ","
        listas = listas[:-1]
        listas = listas + ";"
        for i in self.Extra_values:
            listas = listas + str(i) + ","
        listas = listas[:-1]
        listas = listas + ";"
        return  cabeçalho + listas

    def to_bytes(self):
        novo = message(self.to_string())
        return pickle.dumps(novo)

    def getflags(self):
        return self.flags
    
    def setflags(self,flags):
        self.flags=flags

    def setResponseCode(self,code):
        self.reponsecode=code

    def getQname(self):
        return self.Q_name
    
    def setQname(self,Q_name):
        self.Q_name=Q_name

    def getQtype(self):
        return self.type
    
    def setQtype(self,type):
        self.type = type

    def getResponse_values(self):
        return self.Response_values

    def setResponse_values(self,list):
        self.Response_values=list

    def setn_values(self,n):
        self.n_values=n

    def setAutority_values(self,list):
        self.Autority_values=list

    def setn_authority(self,n):
        self.n_autority=n

    def setExtra_values(self,list):
        self.Extra_values=list

    def setn_extravalues(self,n):
        self.extra_values=n