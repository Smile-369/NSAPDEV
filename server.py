import socket
import threading
from datetime import datetime
import csv
import os

IP = "10.2.201.200"
PORT = 8000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
GET_CSV_MSG = "!GET_CSV"
CSV_FILE = "received_messages.csv"
KILL_SERVER_MSG = "!KILL"

# Initialize the CSV file with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Connection ID", "Timestamp", "Client Address", "Message"])

# Global connection ID counter
connection_id = 0
connection_id_lock = threading.Lock()

def handle_client(conn, addr, conn_id):
    print(f"[NEW CONNECTION] {addr} connected with ID {conn_id}.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([conn_id, date, addr, msg])
            connected = False
        elif msg == GET_CSV_MSG:
            try:
                with open(CSV_FILE, mode='r') as file:
                    while True:
                        csv_data = file.read(SIZE)
                        if not csv_data:
                            break
                        conn.send(csv_data.encode(FORMAT))
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent CSV data to {addr}")
                    conn.close()
            except Exception as e:
                error_msg = f"Error reading CSV file: {str(e)}"
                conn.send(error_msg.encode(FORMAT))
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Write the message to the CSV file
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([conn_id, date, addr, msg])
        print(f"[{date}] | {addr} | ID {conn_id} | {msg}")        
        msg = f"Msg received: {msg}"
        conn.send(msg.encode(FORMAT))

    conn.close()

def main():
    global connection_id
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        with connection_id_lock:
            conn_id = connection_id
            connection_id += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr, conn_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
