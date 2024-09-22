import socket as s

server_address = ("192.168.199.179", 6980)
BUFFER_SIZE = 4092

udp_server_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
udp_server_socket.bind(server_address)

print("*************************\nChat Client-Server: scrivi <arrivederci> per interrompere la connessione\n*************************\n\n")

while True:
    data, address = udp_server_socket.recvfrom(BUFFER_SIZE)
    print(f"{data.decode('utf-8')}, da {address}")

    if(data.decode('utf-8').lower() == "arrivederci"):
        print("Il client ha terminato la connessione...")
        break

    risposta = input("Rispondi al messaggio:  ")
    udp_server_socket.sendto(risposta.encode('utf-8'), address)

    if(risposta.lower() == "arrivederci"):
        print("Il server ha terminato la connessione...")
        break

udp_server_socket.close()