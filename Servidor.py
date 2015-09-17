#-*-encoding: latin1 -*-

import socket
import thread
import select

MAP_CLIENTES = {}
lista = []
LISTA_DE_CLIENTES = []
lista_sockets = []
remetente = 'sacramento '
msgServ = 'Por favor informe nome do usuário: '
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 9000            # Porta que o Servidor esta

def envia(sock, acao, msg):
    for i in MAP_CLIENTES:
        chat = MAP_CLIENTES.get(0)
        if chat != saida:
            if msg.len() == 1:
                con.sendall("olá")
            else:
                print 'mensagem não enivada'
#Manda mensagem para lista de socketes
def broadcast_data (sock, message):
    print lista_sockets
    for i in lista_sockets:
        #print i
        if i != sock:
        #if sock in lista_sockets:
            try:
                print 'enviada...para'
                i.send(message)
            except:
                i.close()
                lista_sockets.remove(i)
        else:
            print'Dado nao enviado....'
#Manda mesagem para mapa de clientes
def broadcast_data_mapa (sock, message):

    for nome, conexao in MAP_CLIENTES.items():
        if conexao != sock:
            try:
                print 'enviada....para'
                conexao.send(message)
            except:
                conexao.close()
                lista_sockets.remove(conexao)
        else:
            print'Dado nao enviado....'


def armazena(novoCliente, nome):
    for i in range(len(LISTA_DE_CLIENTES)):
        if novoCliente == LISTA_DE_CLIENTES[i]:
            return True
    LISTA_DE_CLIENTES.append(novoCliente)
    MAP_CLIENTES.update({novoCliente: nome})
    #MAP_CLIENTES.update({novoCliente: valor})
    return False

def conectados (con):
    con.sendall('Conectados > ')
    for nome, valor in MAP_CLIENTES.items():
        con.sendall('[ '+nome+' ]')

def remove(velhoCliente):
    for i in range(len(LISTA_DE_CLIENTES)):
        if LISTA_DE_CLIENTES[i] == velhoCliente:
            LISTA_DE_CLIENTES.remove(velhoCliente)

def conectado(con, cliente):
    respHost = con.recv(1024)
    #print respHost
    if armazena(respHost, con):
        con.sendall('Cadastro já extistente. Tente outro nome...')
        con.close()
        return
    else:
        print respHost+'  :conectou ao Servidor...'
        con.sendall(respHost+" Conectado...")

    if respHost == ' ':
        return
    if len(LISTA_DE_CLIENTES) == 1:
        con.send('Voce é o primeiro conectado, por favor, aguarde outras conexões para iniciar o chat')
    else:
        conectados(con)
    #print MAP_CLIENTES.values()
    while True:
        try:
            data = con.recv(1024)
            for x, m in MAP_CLIENTES.items():
                if con == m:
                    remetente = x
            if data:
               #broadcast_data(con, "\r"+ str(con.getpeername()) + 'disse: ' + data)
               broadcast_data_mapa(con,remetente+' disse: '+ data)
        except:
            print 'Finalizando conexão do cliente', cliente
            for x, m in MAP_CLIENTES.items():
                if m == con:
                    broadcast_data_mapa(con,'o cliente '+ x +' desconectou...')
                    del MAP_CLIENTES[x]
            con.close()
            thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(5)
print 'Servidor pronto.....'


while True:
    con, cliente = tcp.accept()
    #print con
    #print cliente
    endereco, porta = cliente
    lista_sockets.append(con)
    thread.start_new_thread(conectado, tuple([con, cliente]))
tcp.close()