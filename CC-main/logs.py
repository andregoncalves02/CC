from datetime import datetime

#escreve no file a string
def write_infinal_logs(logs_file,str_e):
    f = open(logs_file, "a")
    f.write(str_e)
    f.close()

#returna a data e as horas 
def data_horas():
    line=datetime.now().strftime('%d:%m:%Y:%H:%M:%S:%MS ')
    return line


#tem uma funçao para cada tipo ddos logs em que mete toda a informaçao numa string e coloca no ficheiro
def queryRE(type, endereco_ip, logs_file,all_logs):
    line = str(data_horas() + type +" "+endereco_ip+"\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def respostaPR(type, endereco_ip, logs_file,all_logs):
    line = str(data_horas() + type + " " + endereco_ip + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logZT(type, endereco_ip, logs_file,all_logs):
    line = str(data_horas() + " ZT" + endereco_ip + " " +type + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logsEV(atividadde, file, logs_file,all_logs):
    line = str(data_horas() + " EV " + "@ " + atividadde + " " +file + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logEZ(type, endereco_ip, logs_file,all_logs):
    line = str(data_horas() + " EZ " + endereco_ip + " " +type + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logsER(endereco_ip, logs_file,all_logs):
    line = str(data_horas() + " ER " + endereco_ip + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logsFL(erro, logs_file,all_logs):
    line = str(data_horas() + " FL " + "127.0.0.1 " + erro + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logsTO(tipo_to, logs_file,all_logs):
    line = str(data_horas() + " TO " + tipo_to + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logsSP(erro, logs_file,all_logs):
    line = str(data_horas() + " SP 127.0.0.1 " + erro + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

def logsST(porta,timeout,modo, logs_file,all_logs):
    line = str(data_horas() + " ST " + "127.0.0.1 " + porta + timeout + modo + "\n")
    write_infinal_logs(logs_file,line)
    write_infinal_logs(all_logs,line)

