import socket as s

udp_client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)

message = b"ciao"

server_address = ("192.168.131.179", 6980)
BUFFER_SIZE = 4092

udp_client_socket.sendto(message, server_address)

data, server_address = udp_client_socket.recvfrom(BUFFER_SIZE)

print(f"Messaggio ricevuto da server: {data.decode()} da {server_address}")