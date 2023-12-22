from datetime import datetime

class cache:
    def __init__(self):
        self.table=[[None,None,None,None,None,None,None,1,0]]
        self.n=1
        self.time_started = datetime.now()
    
    def add_line(self,str,org,default):
        line = str.split()
        n=len(line)
        old_line=[]

        if (org == "others" and n>=4):
            lista =self.find_all((line[0],line[1]))
            for i in lista:
                old_line = self.table[i]
                if n == 5:
                    if old_line[3] == int(line[3]) and old_line[4] == int(line[4]):
                        break
                else:
                    if old_line[3] == int(line[3]) and old_line[4] == -1:
                        break

            if old_line:
                if old_line[5]=="others":
                        timestamp = datetime.now() - self.time_started
                        old_line[6]=timestamp.total_seconds()
                        old_line[8]=1

        if (org != "others" or not old_line):
            for i in self.table:

                if i[8] == 0:
                    old_line=i
                    break
                
            if n >= 4:
                if line[0][-1:] != ".":
                    old_line[0]=line[0] + "." + default
                else:
                    old_line[0]=line[0]
                old_line[1]=line[1]
                old_line[2]=line[2]
                old_line[3]=int(line[3])
            if n== 4:
                old_line[4]=-1
            else:
                old_line[4]=int(line[4])
            
            old_line[5]=org
            timestamp = datetime.now() - self.time_started
            old_line[6]=timestamp.total_seconds()
            old_line[8]=1
            if i[7]== self.n:
                self.n+=1
                self.table.append([None,None,None,None,None,None,None,self.n,0])

    def find(self,index,name,type):
        result = -1
        while result == -1 and index<=self.n:
            if self.table[index-1][8] == 1:
                time = datetime.now() - self.time_started
                if self.table[index-1][3] < time.total_seconds() - self.table[index-1][6]:
                    self.table[index-1] [8] = 0
                elif (self.table[index-1][0] == name and self.table[index-1][1] == type):
                    result = index
            index+=1

        return result

    def find_all(self,tuple_N_T):
        results = []
        i=1
        while  i <= self.n and i > 0:
            i = self.find(i,tuple_N_T[0],tuple_N_T[1])
            if i>0:
                results.append(i)
            i+=1
         
        return results

    def procura(self,name,type):
        listofnames=[]

        lines_response = self.find_all((name,type))
        newlines_response=[]
        for index in lines_response:
            listofnames.append(self.table[index-1][2])
            newlines_response.append(self.table[index-1][0] + " " + self.table[index-1][1] + " " + self.table[index-1][2])
  
        lines_authorities = self.find_all((name,"NS"))
        newlines_authorities=[]
        for index in lines_authorities:
            listofnames.append(self.table[index-1][2])
            newlines_authorities.append(self.table[index-1][0] + " " + self.table[index-1][1] + " " + self.table[index-1][2])
            
        lines_extra=[]
        for name in listofnames:
            lines_extra.append(self.find(1,name,"A"))
        newlines_extras = []
        for index in lines_extra:
            newlines_extras.append(self.table[index-1][0] + " " + self.table[index-1][1] + " " + self.table[index-1][2] )
        return newlines_response,newlines_authorities,newlines_extras

    def procura_reverse(self, ip):
        result = -1
        index=1
        while result == -1 and index <= self.n:
            if self.table[index - 1][8] == 1:
                if (self.table[index - 1][2] == ip and self.table[index - 1][1] == "PTR"):
                    result = index
            index += 1
        if result >= 0:
            return self.table[result-1][0]
        return None

    def procura_sv(self,domain):
        i = self.find(1,domain,"NS")
        if i>0:
            i = self.find(1,self.table[i-1][2],"A")
            if i>0:
                return self.table[i-1][2]

        while domain:
            for l in domain:
                if l == ".":
                    domain = domain.replace(l,"",1)
                    break
                domain = domain.replace(l,"",1)

            i = self.find(1,domain,"NS")
            if i>0:
                i = self.find(1,self.table[i-1][2],"A")
                if i>0:
                    return self.table[i-1][2]
        
        return -1

    def bd_valida(self,name):
        i = self.find(1,name,"SOASPIRE")
        if i >0:
            timestamp = datetime.now() - self.time_started
            if self.table[i][2] > timestamp.total_seconds():
                return True
            else :
                return False
        return False
