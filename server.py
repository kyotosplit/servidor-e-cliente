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