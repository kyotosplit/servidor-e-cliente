import socket
import cv2
import pickle
import struct

def view_screen(host='localhost', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data = b""
    payload_size = struct.calcsize("L")

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        
        packet_msg_size = data[:payload_size]
        data = data[payload_size]
        msg_size = struct.unpack("L", packet_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        screenshot = pickle.loads(frame.data)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        cv2.inshow("rmt screen", frame)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
    
    client_socket.close()

if __name__ == "__main__":
    view_screen()