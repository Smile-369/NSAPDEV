import socket

IP_ESP32 = '192.168.237.105'
PORT_ESP32 = 80

IP_SERVER = socket.gethostbyname(socket.gethostname())
PORT_SERVER = 5566

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP_SERVER, PORT_SERVER))
print(f"[CONNECTED] Client connected to server at {IP_SERVER}:{PORT_SERVER}")

def receive_from_esp32():
    esp32 = socket.socket()
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
                msg = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER] {msg}")

    except socket.error as e:
        print(f"[ESP32] {e}")
    except KeyboardInterrupt:
        print("[ESP32] KeyboardInterrupt")
    finally:
        esp32.close()

def main():

    while True:
        receive_from_esp32()

if __name__ == "__main__":
    main()
