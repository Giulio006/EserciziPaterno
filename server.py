import socket as s              #se non scrivessi as s dovrei scrivere socket.metodo(), invece ora scrivo s.metodo()

server_address = ("192.168.1.15", 6980)          #ip del SERVER + porta usata (deve essere un valore alto)
BUFFER_SIZE = 4092              #dimensione massima del buffer per i dati ricevuti

udp_server_socket = s.socket(s.AF_INET, s.SOCK_DGRAM) #s.AF_INET significa che usiamo IPv4, s.SOCK_DGRAM significa che siamo in udp
udp_server_socket.bind(server_address)          #associamo il server all'indirizzo e alla porta prima specificati

data, address = udp_server_socket.recvfrom(BUFFER_SIZE)         #aspetta di ricevere messaggi (data = messaggio, address = IP DEL CLIENT)
print(f"Messaggio ricevuto: {data.decode('utf8')} da {address}")

udp_server_socket.sendto("Benvenuto!!!".encode("utf-8"), address)       #mando un messaggio al client in formato byte (encode("utf-8") -> mi serve l'ip del client -> address)
udp_server_socket.close()       #chiudo il server e termino la comunicazione