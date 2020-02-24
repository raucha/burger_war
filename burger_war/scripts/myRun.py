#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
import rosparam
import tf

from geometry_msgs.msg import Twist
import actionlib # RESPECT @seigot
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal # RESPECT @seigot

#from std_msgs.msg import String
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import cv2


class RandomBot():
    def __init__(self, bot_name):
        # bot name
        self.name = bot_name
        # velocity publisher
        # self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        self.my_color = rospy.get_param('~rside')
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction) # RESPECT @seigot]


    def setGoal(self,x,y,yaw):
        # RESPECT @seigot
        self.client.wait_for_server()
        #print('setGoal x=', x, 'y=', y, 'yaw=', yaw)

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        # name = 'red_bot' if self.my_color == 'r' else 'blue_bot'
        # goal.target_pose.header.frame_id = name + '/map' if self.sim_flag == True else 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

        # Euler to Quartanion
        q=tf.transformations.quaternion_from_euler(0,0,yaw)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        ret = self.client.send_goal_and_wait(goal, execute_timeout=rospy.Duration(4))
        return ("PENDING" ,"ACTIVE" ,"RECALLED" ,"REJECTED" ,"PREEMPTED" ,"ABORTED" ,"SUCCEEDED" ,"LOST")[ret]


    def strategy(self):
        r = rospy.Rate(10) # change speed 1fps

        while not rospy.is_shutdown():
            state = self.setGoal(-0.5, 0, 0)
            rospy.loginfo(state)
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('my_run')
    bot = RandomBot('myRun')
    bot.strategy()

