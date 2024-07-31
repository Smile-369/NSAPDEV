import socket
import threading

IP_ESP32 = '192.168.1.5'
PORT_ESP32 = 80

IP_SERVER = "ccscloud.dlsu.edu.ph"
PORT_SERVER = 20257

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
GET_CSV_MSG = "!GET_CSV"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP_SERVER, PORT_SERVER))
print(f"[CONNECTED] Client connected to server at {IP_SERVER}:{PORT_SERVER}")

def receive_from_esp32():
    esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    esp32.connect((IP_ESP32, PORT_ESP32))

    try:
        while True:
            msg = esp32.recv(1024)
            if not msg:
                break
            msg = msg.decode().strip()
            if msg:
                print(f"[ESP32] {msg}")
                client.send(msg.encode(FORMAT))
                response = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER] {response}")

    except socket.error as e:
        print(f"[ESP32] {e}")
    except KeyboardInterrupt:
        print("[ESP32] KeyboardInterrupt")
    finally:
        esp32.close()

def request_csv():
    client.send(GET_CSV_MSG.encode(FORMAT))
    receive_csv()

def receive_csv():
    with open("received_messages_from_server.csv", mode='wb') as file:
        while True:
            data = client.recv(SIZE)
            if not data:
                break
            file.write(data)
    print("CSV file received and saved as 'received_messages_from_server.csv'.")

def main():
    esp32_thread = None

    while True:
        user_input = input("Enter command (start, get_csv, disconnect): ").strip().lower()
        if user_input == "start":
            if esp32_thread is None or not esp32_thread.is_alive():
                esp32_thread = threading.Thread(target=receive_from_esp32)
                esp32_thread.start()
                print("[INFO] ESP32 thread started.")
            else:
                print("[INFO] ESP32 thread is already running.")
        elif user_input == "get_csv":
            request_csv()
        elif user_input == "disconnect":
            client.send(DISCONNECT_MSG.encode(FORMAT))
            print("[DISCONNECTED] Client disconnected from server.")
            break
        else:
            print("Unknown command. Please use 'start', 'get_csv', or 'disconnect'.")

    client.close()

if __name__ == "__main__":
    main()
