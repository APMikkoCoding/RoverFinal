import move_data
import network
import socket
import pickle
import cv2
from Depth import main as Depth
import Images
import Pathfinding

class Server:
    def __init__(self, width, height):
        self.connection = None
        self.server_socket = None
        self.SOCKET_ADDRESS = None
        self.width = width
        self.height = height
        self.known_points = []
        self.path = Pathfinding.find_path(self.width, self.height, start=(0,0), known_points=self.known_points)
        self.step_num = 0
        self.ns = 1
        self.ew = 0

    def step(self):
        
        current_frame = self.receive_frame()
        current_pos = self.path[self.step_num]
        closest = Depth.find_depth(current_frame).max()
        if closest >= TEST_NUMBER: # WE NEED TO TEST NUMBER
            objects = Images.evauluate_image(cv2.imwrite('current.png', current_frame))
            pass

        self.step_num +=1
        self.path = Pathfinding.find_path(self.width, self.height, start=(0,0), known_points=self.known_points)
             # Edit 2d map
        # VVV PUT MOVE LOGIC IN THIS VVV
        #move = self.process_movement()
        # ^^^ PUT MOVE LOGIC IN THIS ^^^

        self.send_movement(move)

        cv2.imshow("Stream", current_frame)
        if cv2.waitKey(1) == ord('q'): quit(0)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)  # "192.168.43.105"

        print("IP: ", host_ip)

        self.SOCKET_ADDRESS = (host_ip, network.PORT)

        self.server_socket.bind(self.SOCKET_ADDRESS)
        self.server_socket.listen(5)
        print("Listening.")

        self.connection, _ = self.server_socket.accept()

    def receive_frame(self):
        header = self.connection.recv(network.HEADER_LENGTH).decode(network.HEADER_FORMAT)

        if header:
            data = b''

            while True:
                data += self.connection.recv(int(header))
                if data[-len(network.END):] == network.END: break

            return pickle.loads(data)
            # ^^^ This is the frame ^^^

    #def process_movement(self) -> MoveData:
    #    return MoveData() # Replace with real code

    def send_movement(self, move_data):
        move_bytes = pickle.dumps(move_data)

        header = str(len(move_bytes)).encode(network.HEADER_FORMAT)
        header += b' ' * (network.HEADER_LENGTH - len(header))
        self.connection.send(header)

        self.connection.sendall(move_bytes + network.END)