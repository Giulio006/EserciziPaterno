import socket as s

udp_client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)

server_address = ("192.168.1.15", 6980)
BUFFER_SIZE = 4092

print("*************************\nChat Client-Server: scrivi <arrivederci> per interrompere la connessione\n*************************\n\n")

while True:
    messaggio = input("Manda un messaggio al server:    ")
    udp_client_socket.sendto(messaggio.encode('utf-8'), server_address)

    if(messaggio.lower() == "arrivederci"):
        print("Il client ha terminato la connessione...")
        break

    data, address = udp_client_socket.recvfrom(BUFFER_SIZE)
    print(f"{data.decode('utf-8')}, da {address}")

    if(data.decode('utf-8').lower() == "arrivederci"):
        print("Il server ha terminato la connessione...")
        break

udp_client_socket.close()