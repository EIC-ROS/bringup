#!/usr/bin/env python
import rospy
import socket
import struct
from std_msgs.msg import Float32, Header
from lift_controller.srv import Demand_position, Demand_positionRequest, Demand_positionResponse
from sensor_msgs.msg import JointState

class lift_client :
    def __init__(self) -> None :
        print("run lift_client class")
        rospy.wait_for_service("/lift/set_position")
        
        self.client = rospy.ServiceProxy('/lift/set_position', Demand_position)
        self.pub = rospy.Publisher('lift_state', JointState, queue_size=10)
        rospy.sleep(0.1)
        
        self.lift_state = JointState()
        self.lift_state.name = ['lift_joint']


    def go_to(self, pos:float) :
        resp:Demand_positionResponse = self.client(pos)
        
        self.lift_state.position = [resp.confident_position]
        self.pub.publish(self.lift_state)

        return resp.confident_position
    
    def set_zero(self) :
        return self.go_to(float(-100.0))

    def set_position(self, pos) :
        return self.go_to(pos)
    
    def set_max(self) :
        return self.go_to(float(100.0))

if __name__ == "__main__" :
    print("run lift_client_node")
    rospy.init_node("lift_client_node")
    lift = lift_client()
    print(lift.set_zero())
    # lift.set_position(float(input("position : ")))
    lift.set_max()