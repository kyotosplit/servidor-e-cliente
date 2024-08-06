import socket
import threading
import pyautogui
import pickle
import struct

def capture_screen():
    screenshot = pyautogui.screenshot()
    return screenshot

def handle_client(client_socket):
    while True:
        screenshot = capture_screen()
        data = pickle.dumps(screenshot)
        message_size = struct.pack("L", len(data))
        client_socket.sendall(message_size + data)
    
def start_server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()