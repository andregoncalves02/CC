#Esta funçao receve o caminho para um ficheiro um tipo
#(config-sifnica que vai ler de um ficheiro de configuraçao e guardar os valores lidos no servidor ou db-ifnica que vai ler de um ficheiro de bases de dados e guardar na cache)
#e o servidor em causa para poder guardar as informaçoes do ficheiro config ou aceder a cache e guardar la a informaçao
def leitor_file(tipo,file,server):
    f=open(file,'r')
    for line in f:
        lista_line = line.split()
        if lista_line != None:
            if(len(lista_line)>0):
                frs = lista_line[0]
                if frs!="#" and frs!="\n":
                    leitor(tipo,lista_line,server)

#esta funçao é uma auxiliar de cima que tem a mesma utilidade mas recebe ja a linha do ficheiro e descodifica-a
def leitor(tipo,lista_line,server):
    if tipo=="config":
        if len(lista_line) > 2:
            if lista_line[1] == "DB":
                server.setFileDB(lista_line[2])
            elif lista_line[1] == "SS":
                server.setipSS(lista_line[2])
            elif lista_line[1] == "SP":
                server.setipSP(lista_line[2])
            elif lista_line[1] == "DD":
                server.setDD(lista_line[2])
            elif lista_line[1] == "ST":
                aux=[]
                f=open(lista_line[2],"r")
                for line in f:
                    aux.append(line.strip())
                server.setlistaSTS(aux)
            elif lista_line[1] == "LG" and lista_line[0] != "all":
                server.setlogs(lista_line[2])
            elif lista_line[1] == "LG":
                server.setalllogs(lista_line[2])

def leitor_cache(file,server,org):
    f=open(file,'r')
    TTL = 0
    Default=("","")
    for line in f:
        lista_line = line.split()
        if lista_line != None:
            n=len(lista_line)
            if(n>0):
                frs = lista_line[0]
                if frs!="#" and frs!="\n":
                    if n == 3:
                        if lista_line[0] == "TTL":
                            TTL = lista_line[2]
                        elif lista_line[1] == "DEFAULT":
                            Default=(lista_line[0],lista_line[2])
                    else:
                        server.addto_cache(line.replace(Default[0],Default[1]).replace("TTL",TTL),org,Default[1])

def leitor_cache_line(lines,server,org):
    TTL = 0
    Default=("","")
    for line in lines:
        lista_line = line.split()
        if lista_line != None:
            n=len(lista_line)
            if(n>0):
                del(lista_line[0])
        if lista_line != None:
            n=len(lista_line)
            if(n>0):
                frs = lista_line[0]
                if frs!="#" and frs!="\n":
                    if n == 3:
                        if lista_line[0] == "TTL":
                            TTL = lista_line[2]
                        elif lista_line[1] == "DEFAULT":
                            Default=(lista_line[0],lista_line[2])
                    else:
                        line = " ".join(lista_line)
                        server.addto_cache(line.replace(Default[0],Default[1]).replace("TTL",TTL),org,Default[1])
                        
