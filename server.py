import socket
import threading
import pyautogui
import pickle
import struct

def capture_screen():
    try:
        screenshot = pyautogui.screenshot()
        return screenshot
    except Exception as e:
        print(f"erro ao capturar a tela: {e}")
        return None

def handle_client(client_socket):
    while True:
        screenshot = capture_screen()
        if screenshot is None:
            continue
        
        screenshot = screenshot.convert("RGB")
        
        data = pickle.dumps(screenshot)
        message_size = struct.pack("L", len(data))
        try:
            client_socket.sendall(message_size + data)
        except Exception as e:
            print(f"erro ao enviar dados para o cliente: {e}")
            break

def start_server(host='0.0.0.0', port=9998):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"baguncinha on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"e.e {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
