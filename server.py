import socket
import threading
from datetime import datetime
import csv

IP = "10.2.201.200"
PORT = 8000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
GET_CSV_MSG = "!GET_CSV"
CSV_FILE = "received_messages.csv"

with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Client Address", "Message"])

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        elif msg == GET_CSV_MSG:
            send_csv(conn)
        else:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{date}] | {addr} {msg}")
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, addr, msg])
            response = f"Msg received: {msg}"
            conn.send(response.encode(FORMAT))

    conn.close()

def send_csv(conn):
    with open(CSV_FILE, mode='rb') as file:
        conn.sendall(file.read())

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
