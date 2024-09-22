import socket as s

server_address = ("192.168.1.15", 6980)
BUFFER_SIZE = 4092

udp_server_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
udp_server_socket.bind(server_address)

for i in range(10):
    data, address = udp_server_socket.recvfrom(BUFFER_SIZE)
    print(f"Messaggio ricevuto: {data.decode('utf8')} da {address}")

udp_server_socket.sendto("Messaggi ricevuti!!!".encode("utf-8"), address)
udp_server_socket.close()