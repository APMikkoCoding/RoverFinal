import pickle
import cv2
import Modules.Server.Server.move_data as move_data
import network
import socket
import sys
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors

CAM_RESOLUTION_WIDTH = 800
CAM_RESOLUTION_HEIGHT = 600

class Movement:
    def __init__(self):
        rvr = SpheroRvrObserver()
        rvr.wake()

class Client:
    def __init__(self):
        self.client_socket = None
        self.cam = None
        self.movement = Movement()

    def start(self, host_ip):
        # socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host_ip, network.PORT))

        # camera
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_RESOLUTION_WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_RESOLUTION_HEIGHT)

        if not self.cam.isOpened():
            print("Cannot open camera")
            exit()

    def send_frame(self, frame):
        frame_data = pickle.dumps(frame)

        header = str(len(frame_data)).encode(network.HEADER_FORMAT)
        header += b' ' * (network.HEADER_LENGTH - len(header))
        self.client_socket.send(header)

        self.client_socket.sendall(frame_data + network.END)

    def step(self):
        did_read_frame, frame = self.cam.read()

        if not did_read_frame:
            print("Frame did not read, stream might have ended. Exiting.")
            exit(0)

        self.send_frame(frame)
        movement = self.receive_movement()
        self.move(movement)

    def move(self, movement):
        self.movement.rvr.drive_control.drive_forward_seconds(speed=movement[0], heading=movement[1], time_to_drive=movement[2]) # implement

    def receive_movement(self) -> move_data.MoveData:
        header = self.client_socket.recv(network.HEADER_LENGTH).decode(network.HEADER_FORMAT)

        if header:
            data = b''

            while True:
                data += self.client_socket.recv(int(header))
                if data[-len(network.END):] == network.END: break

            return pickle.loads(data)
            # ^^^ This is the frame ^^^