#-*-encoding: latin1 -*-
import socket
import thread

def run():
   try:

      while True:
          msg = clienteTcp.recv(1024)
          if msg == ' ':
            print "Conexão encerrada..."
            clienteTcp.close()
          print msg
          print "Responder > "
   except:
      print "Ocorreu uma falha no servidor... "

if __name__ == "__main__":
    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 9000            # Porta que o Servidor esta
    clienteTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    clienteTcp.connect(dest)
    #mensagem=raw_input()
        #if len(mensagem) <= 64:
            #self.cliente.send(bytes(mensagem))
        #else:
            #print'erro no tamanho da mensagem'

    try:
        teclado = raw_input("Digite seu nome: ")
        teclado = teclado.upper()
        clienteTcp.sendall(teclado)
        thread.start_new_thread(run,())
        while True:
            msg = raw_input('Mensagem > ')
            clienteTcp.sendall(msg)
    except:
        print "Falha na conexão... "
        clienteTcp.close()
        thread.exit()