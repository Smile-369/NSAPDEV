import socket
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

IP_SERVER = "ccscloud.dlsu.edu.ph"
PORT_SERVER = 20257
RECIEVECSV_MSG = "!GET_CSV"
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
received_csv = "received.csv"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP_SERVER, PORT_SERVER))
print(f"[CONNECTED] Client connected to server at {IP_SERVER}:{PORT_SERVER}")

def plot_csv_data(filename):
    data = pd.read_csv(filename)
    motion_data = data[data['Message'] == 'Motion detected!']
    client_motion_counts = motion_data['Connection ID'].value_counts()
    plt.figure(figsize=(10, 6))
    client_motion_counts.plot(kind='bar')
    plt.xlabel('Client ID')
    plt.ylabel('Motion Detected Count')
    plt.title('Motion Detected Counts by Client ID')
    plt.show()

def esp32_emulator(client_id):
    esp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    esp_client.connect((IP_SERVER, PORT_SERVER))
    while True:
        message = "Motion detected!"
        esp_client.send(message.encode(FORMAT))
        time.sleep(1)

def start_emulators():
    threads = []
    for i in range(10):
        t = threading.Thread(target=esp32_emulator, args=(i,))
        t.start()
        threads.append(t)

def main():
    while True:
        msg = input("Enter message: ")
        if msg == RECIEVECSV_MSG:
            client.send(msg.encode(FORMAT))
            with open(received_csv, "wb") as file:
                while True:
                    data = client.recv(SIZE)
                    print(data.decode('utf-8'))
                    if not data:
                        break
                    file.write(data)
            print(f"[SERVER] CSV data received and saved to {received_csv}")
            plot_csv_data(received_csv)

        elif msg == DISCONNECT_MSG:
            client.send(msg.encode(FORMAT))
            break
        elif msg == "!START_EMULATORS":
            threading.Thread(target=start_emulators).start()
        else:
            client.send(msg.encode(FORMAT))
            response = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {response}")

if __name__ == "__main__":
    main()
