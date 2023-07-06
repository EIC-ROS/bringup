import rospy
import socket
import struct
from std_msgs.msg import Float32
from lift_controller.srv import Demand_position, Demand_positionRequest, Demand_positionResponse

class lift_socket:
    demand_position = 0
    max_position = 17.0
    min_position = 0.0

    def __init__(self, host:str, port:int) -> None:
        print("run lift_socket class")
        self.host = host
        self.port = port
        
        # print("declare client socket")
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("before connect to ESP32")
        # self.client_socket.connect((self.host, self.port))
        # print("Connected to ESP32")

        rospy.Service("/lift/set_position",Demand_position,self.request_position)

    def request_position(self,req:Demand_positionRequest):
        print("run request_position function")
        res = Demand_positionResponse()
        self.demand_position = req.demand_position

        if self.demand_position > self.max_position:
            res.confident_position = self.max_position
        elif self.demand_position < self.min_position:
            res.confident_position = self.min_position
        else:
            res.confident_position = self.demand_position
        
        res.send = True
        return res
            
    
    def run(self):
        print("run run function")
        while not rospy.is_shutdown():
            try:
                i = 1

                while not rospy.is_shutdown():
                    # self.client_socket.send(struct.pack('!f', self.demand_position))
                    print("Sent:", self.demand_position, "Iter:",i) 
                    
                    rospy.sleep(1)
                    
                    # use for reconnect i = 10000
                    # if i == 100 :
                    #     client_socket.close()

                    i += 1
                    
            # except (socket.error, ConnectionResetError):
            #     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     self.client_socket.connect((self.host, self.port))
            #     print("Reconnecting")
            #     continue

            except KeyboardInterrupt:
                self.client_socket.close()
                rospy.signal_shutdown("shutdown node")
                break

if __name__ == "__main__":
    print("run lift_controller_node")
    rospy.init_node("lift_server_node")
    lift_server = lift_socket("10.10.10.3",9090)
    lift_server.run()