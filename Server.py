# -*- coding: cp1252 -*-
from socket import *
import os

CLIENTES = ["Bernardo", "Carlos", "Joao"]

SUCESSO = "OK"
FALHA = "NOK"
APRESENTACAO = "CUMP"
LISTAGEM = "LIST"
TERMINAR = "TERM"
PEGA = "PEGA"

esperando = True
terminar_conexao = False


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print("Servidor pronto para receber requisições.")

def listar_arquivos():
    lista = []
    for root, dirs, files in os.walk('.\\Arquivos', topdown=True):
        dirs.clear() #with topdown true, this will prevent walk from going into subs
        for file in files:
          #do some stuff
          lista.append(file)
    return lista

def executar(entrada):
    try:
        lista = entrada.split(" ",2)
        global esperando
        global terminar_conexao
        if (lista[1] == APRESENTACAO and esperando == True and len(lista) == 3):
            seq_numero = int(lista[0])
            if lista[2] in CLIENTES:
                esperando = False
                return (str(seq_numero) + ' ' + SUCESSO).encode(),False
            terminar_conexao = True
            return (str(seq_numero) + ' ' + FALHA).encode(), False
        elif (lista[1] == LISTAGEM and esperando == False and len(lista) == 2):
            listarquivos = listar_arquivos()
            seq_numero = int(lista[0])
            if len(listarquivos) == 0:
                return (str(seq_numero) + ' ' + FALHA).encode(), False
            return (str(seq_numero) + ' ARQS '+ str(len(listarquivos)) + ' ' + ','.join(listarquivos)).encode(), False
        elif (lista[1] == PEGA and esperando == False and len(lista) == 3):
            txt_arquivo = lista[2]
            arquivo = txt_arquivo.split(" ",1)[0]
            seq_numero = int(lista[0])
            lista_arqs = listar_arquivos()
            if (arquivo not in lista_arqs) or len(lista_arqs) == 0:
                return (str(seq_numero) + ' ' + FALHA).encode(), False
            tamanho_bytes = os.path.getsize('./Arquivos/'+arquivo)
            arq = open(os.path.join('./Arquivos', arquivo), "rb").read()
            return (str(seq_numero) + ' ARQ ' + str(tamanho_bytes) + ' ').encode() + arq, False
        elif (lista[1] == TERMINAR and esperando == False and len(lista) == 2):
            seq_numero = int(lista[0])
            terminar_conexao = True
            return (str(seq_numero) + ' ' + SUCESSO).encode(), True
        else:
            seq_num = int(lista[0])
            return (str(seq_num) + " " + FALHA).encode(), False
    except Exception as e:
        print(e)
        return (FALHA).encode(), False

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        terminar_conexao = False
        while True:
            try:
                sentenca = connectionSocket.recv(1024).decode('UTF-8')
                print(sentenca)
                resposta, terminar = executar(sentenca)
                connectionSocket.send(resposta)
                if terminar:
                    esperando = True
                if terminar_conexao == True:
                    esperando = True
                    break
            except Exception as e:
                print(e)
                esperando = True
                break
        connectionSocket.close()
    except (KeyboardInterrupt, SystemExit):
        break

serverSocket.close()
