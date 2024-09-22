import socket as s

udp_client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)          #oggetto socket

message = b"ciao"           #la b è per trasformare il messaggio in formato bytes, richiesto nell'udp

server_address = ("192.168.1.15", 6980)          #DEL SERVER
BUFFER_SIZE = 4092

udp_client_socket.sendto(message, server_address)       #mando al server il messaggio "ciao"

data, server_address = udp_client_socket.recvfrom(BUFFER_SIZE)      #ricevo la risposta del server (data = messaggio ricevuto, server_address è l'indirizzo del server che ha risposto)

print(f"Messaggio ricevuto da server: {data.decode()} da {server_address}")     #mi serve il decode perché data è in formato bytes