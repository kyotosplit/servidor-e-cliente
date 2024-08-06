import socket
import cv2
import pickle
import struct
import numpy as np

def view_screen(host='localhost', port=9998):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data = b""
    payload_size = struct.calcsize("L")

    cv2.namedWindow("a putaria", cv2.WINDOW_NORMAL)

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet

        if len(data) < payload_size:
            break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet

        if len(data) < msg_size:
            break

        frame_data = data[:msg_size]
        data = data[msg_size:]

        screenshot = pickle.loads(frame_data)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        cv2.imshow("a putaria", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    view_screen()
