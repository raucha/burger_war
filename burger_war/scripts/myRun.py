#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
import rosparam

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
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        self.my_color = rosparam.get_param('rside')
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction) # RESPECT @seigot]

    def ssetGoal(self,x,y,yaw):
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

        ret = self.client.send_goal_and_wait(goal, execute_timeout=rospy.Duration(4))
        rospy.loginfo(ret)
        return ret


    def calcTwist(self):
        value = random.randint(1,1000)
        if value < 250:
            x = 0.2
            th = 0
        elif value < 500:
            x = -0.2
            th = 0
        elif value < 750:
            x = 0
            th = 1
        elif value < 1000:
            x = 0
            th = -1
        else:
            x = 0
            th = 0
        twist = Twist()
        twist.linear.x = x; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
        return twist

    def main(self):
        r = rospy.Rate(1) # change speed 1fps

        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0

        while not rospy.is_shutdown():
            twist = self.calcTwist()
            print(twist)
            self.vel_pub.publish(twist)

            r.sleep()


if __name__ == '__main__':
    rospy.init_node('my_run')
    bot = RandomBot('myRun')
    bot.main()

