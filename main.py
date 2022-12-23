# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from blockchain import Blockchain
from api import Api
import random

hostName = "localhost"
serverPort = 8080

class BlockchainServer(BaseHTTPRequestHandler):
    # Change this GET Request to Serve infos to frontend
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>https://pythonbasics.org</title></head>".encode("utf-8"))
        self.wfile.write("<p>Request: %s</p>" % self.path.encode("utf-8"))
        self.wfile.write("<body>".encode("utf-8"))
        self.wfile.write("<p>This is an example web server.</p>".encode("utf-8"))
        self.wfile.write("</body></html>".encode("utf-8"))

     # Crete POST Request to Insert Transaction

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), BlockchainServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    print("Running blockchain...")

    blockchain = Blockchain()
    api = Api()

    api.connect()

    menu_options = {
        1: 'Obter Blockchain',
        2: 'Criar Transação',
        3: 'Encerrar Bloco',
        4: 'Exit',
    }

    def print_menu():
        for key in menu_options.keys():
            print (key, '--', menu_options[key] )

    try:

        # webServer.serve_forever()

        while(True):
            print_menu()
            option = int(input('Enter your choice: '))
            if option == 1:
                chain = api.getChain()
                print(chain)
            elif option == 2:
                sender = str(input('Digite seu nome: \n'))
                recipient = str(input('Digite o nome do destinatário: \n'))
                amount = float(input('Informe a quantidade a ser enviada: \n'))
                blockchain.new_transaction(sender=sender, recipient=recipient, data=amount)
                print('Transação Registrada com sucesso!\n')
            elif option == 3:
                newBlock = blockchain.new_block(proof=random.randint(0,1000000000), previous_hash=None)
                print('Bloco anterior com hash: ' + newBlock['previous_hash'] + ' encerrado\n')
                print('Novo bloco com hash: ' + newBlock['hash'] + ' criado :)\n')
            elif option == 4:
                print('Obrigado!')
                exit()
            else:
                print('Opção inválida :/')

    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")