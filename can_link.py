#!/usr/bin/env python

import can
import rospy
import threading
import numpy as np
from datetime import datetime
from threading import Timer
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped


class AicarCanLink:

    def __init__(self, channel, bitrate):
        # can interface init
        self.can.rc['interface'] = 'socketcan_native'
        self.can.rc['channel'] = channel
        self.can.rc['bitrate'] = bitrate
        # can message id
        self.TWIST_LINEAR_XY = 0x01
        self.TWIST_LINEAR_Z = 0x02
        # ros init
        rospy.init_node("aicar_ros_interface")
        # publish topics define
        self.odom_pub = rospy.Publisher(
            "/aicar/fusion_odometry",
            Odometry,
            queue_size=5)
        # subscribe topics define
        self.cmd_vel_sub = rospy.Subscriber(
            "/aicar/cmd_vel",
            TwistStamped,
            self.cmd_vel_sub_callback)

        rospy.spin()

    def send(self, id, data):
        bus = can.interface.Bus()

        # message wrapper
        msg = can.Message(arbitration_id=id,
                          data=[data[0],
                                data[1],
                                data[2],
                                data[3],
                                data[4],
                                data[5],
                                data[6],
                                data[7]],
                          extended_id=False)
        # send message
        try:
            bus.send(msg)
        except can.CanError:
            print("Message NOT sent!!!")

    def recv(self, timeout):
        bus = can.interface.Bus()
        msg = bus.recv(timeout)
        return msg

    def aicar_topic_advertise_thread(self, seconds, pub, msg):
        # set ros message timestamp
        msg.header.stamp = rospy.Time.now()
        pub.publish(msg)
        # create timer
        sub_topic_thread = Timer(
            seconds,
            self.aicar_topic_advertise_thread,
            (seconds,
             pub,
             msg,
             ))
        sub_topic_thread.start()
        # print('active thread is {}'.format(threading.activeCount()))

    def cmd_vel_sub_callback(self, msg):
        # parse cmd_vel params
        cmd_vel = np.zeros(4, dtype=np.float32)
        cmd_vel[0] = msg.linear.x
        cmd_vel[1] = msg.linear.y
        cmd_vel[2] = msg.angular.z
        cmd_vel[3] = 0
        # pack cmd_vel message
        cmd_vel_uint8 = self.message_pack(cmd_vel)
        # send cmd_vel_linear_x cmd_vel_linear_y
        self.send(self.TWIST_LINEAR_XY, cmd_vel_uint8[:8])
        # send cmd_vel_angular_z
        self.send(self.TWIST_LINEAR_Z, cmd_vel_uint8[8:])

    def message_pack(self, msg):
        data = np.array(msg, dtype=np.float32)
        data.dtype = 'uint8'
        return data

if __name__ == '__main__':
    # TODO
    print("can_link test")
