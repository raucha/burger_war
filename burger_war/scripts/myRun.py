#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
import rosparam
import tf
from math import radians, degrees, atan2
import tf2_ros

from geometry_msgs.msg import Twist, TransformStamped
from actionlib import SimpleActionClient, GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  # RESPECT @seigot
import actionlib

#from std_msgs.msg import String
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import cv2


def get_goals(my_color):
    if my_color == 'b':
        symbol = -1
        th = 180
    else:
        symbol = 1
        th = 0

    # 12x3 (x,y,yaw)
    TARGET = [
        [symbol*-0.8, symbol*0.4, radians(-10+th)],
        [symbol*-0.8, symbol*-0.4, radians(-10+th)],
        [symbol*-0.5, symbol*0, radians(0+th)],
        [symbol*-0.5, symbol*0, radians(-45+th)],
        [symbol*0, symbol*-0.5, radians(180+th)],
        [symbol*0, symbol*-0.5, radians(90+th)],
        [symbol*0., symbol*-0.5, radians(0+th)],
        [symbol*0, symbol*-0.5, radians(-45+th)],
        [symbol*0.4, symbol*-1.0, radians(45+th)],
        [symbol*1, symbol*-0.5, radians(180+th)],
        [symbol*1, symbol*-0.5, radians(45+th)],
        [symbol*1.46, symbol*0, radians(45+th)],  # top
        [symbol*1.46, symbol*0, radians(135+th)],
        [symbol*1, symbol*0.5, radians(180+th)],
        [symbol*1, symbol*0.5, radians(135+th)],
        [symbol*0.4, symbol*1.0, radians(135+th)],
        [symbol*0.4, symbol*1.0, radians(-135+th)],
        [symbol*0, symbol*0.5, radians(0+th)],
        [symbol*0, symbol*0.5, radians(-90+th)],
        [symbol*0, symbol*0.5, radians(180+th)],
        [symbol*0, symbol*0.5, radians(135+th)],
    ]
    return TARGET


def num2mvstate(i):
    return ["PENDING", "ACTIVE", "RECALLED", "REJECTED", "PREEMPTED", "ABORTED", "SUCCEEDED", "LOST"][i]


class RandomBot():
    def __init__(self, bot_name):
        self.name = bot_name
        self.my_color = rospy.get_param('~rside')

        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        self.tfBuffer = tf2_ros.Buffer()
        _ = tf2_ros.TransformListener(self.tfBuffer)
        self.client = actionlib.SimpleActionClient(
            'move_base', MoveBaseAction)  # RESPECT @seigot]
        self.goalcounter = 0
        self.goalcounter_prev = -1
        self.goals = get_goals(self.my_color)

    def setGoal(self, x, y, yaw):
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
        q = tf.transformations.quaternion_from_euler(0, 0, yaw)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]


        def active_cb():
            pass
            # rospy.loginfo("active_cb. Goal pose is now being processed by the Action Server...")

        def feedback_cb( feedback):
            pass
            #To print current pose at each feedback:
            #rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
            # rospy.loginfo("feedback_cb. Feedback for goal pose received{}".format(feedback))

        # def done_cb(result):
        def done_cb(status, result):
            if status is not GoalStatus.PREEMPTED:
                self.goalcounter += 1
                self.goalcounter %= 20
            rospy.loginfo("done_cb. status:{} result:{}".format(num2mvstate(status), result))


        self.client.send_goal(goal, done_cb=done_cb, active_cb=active_cb, feedback_cb=feedback_cb)
        return
        # ret = self.client.send_goal_and_wait( goal, execute_timeout=rospy.Duration(4))
        # return ("PENDING", "ACTIVE", "RECALLED", "REJECTED", "PREEMPTED", "ABORTED", "SUCCEEDED", "LOST")[ret]

    def strategy(self):
        r = rospy.Rate(10)  # change speed 1fps

        # self.setGoal(
        #     self.goals[0][0], self.goals[0][1], self.goals[0][2])
        # print "begin"
        self.setGoal(
            self.goals[0][0], self.goals[0][1], self.goals[0][2])
        # print "end"

        is_patrol_mode_prev = False
        is_patrol_mode = True

        while not rospy.is_shutdown():
            r.sleep()
            # self.client.wait_for_result()
            # value = rospy.get_time()
            # rospy.loginfo("is_patrol_mode:{}".format(is_patrol_mode) )

            is_enemy_detected, enemy_dist, enemy_rad = self.getEnemyDistRad()
            # rospy.loginfo("enemy_dist:{}  enemy_rad:{}".format(enemy_dist, enemy_rad) )
            
            # rospy.loginfo("is_enemy_detected:{} enemy_dist{} enemy_rad:{}".format(is_enemy_detected, enemy_dist, enemy_rad))
            is_patrol_mode = True
            if not is_enemy_detected:
                is_patrol_mode = True
            elif is_patrol_mode and  0.6 > enemy_dist:
                is_patrol_mode = False
            elif not is_patrol_mode and 0.7 < enemy_dist:
                is_patrol_mode = True

            if is_patrol_mode and (not is_patrol_mode_prev or (self.goalcounter is not self.goalcounter_prev)):
            # if is_patrol_mode is True:
                # 巡回モードに切り替わった時、及びゴール座標が変わった時だけ
                # if self.client.get_state() is not GoalStatus.PENDING: 
                self.setGoal(self.goals[self.goalcounter][0], self.goals[self.goalcounter][1], self.goals[self.goalcounter][2])
                rospy.loginfo( num2mvstate(self.client.get_state()))
                self.goalcounter_prev = self.goalcounter
                # if self.client.get_state() not in (GoalStatus.ACTIVE, GoalStatus.PENDING) :
                # # if self.client.get_state() == GoalStatus.SUCCEEDED or self.client.get_state() == GoalStatus.RECALLED:
                #     self.goalcounter += 1
                #     self.goalcounter %= 20
            elif is_patrol_mode:
                # 巡回モード最中。CBが来るまで何もしない。
                pass
            else : 
                # 敵の方向を向くモード
                self.client.cancel_all_goals()
                twist = Twist()
                twist.angular.z = radians(2.0*degrees(enemy_rad))
                self.vel_pub.publish(twist)
            is_patrol_mode_prev = is_patrol_mode


    def getEnemyDistRad(self):
        try:
            # <class 'geometry_msgs.msg._TransformStamped.TransformStamped'>
            trans_stamped = self.tfBuffer.lookup_transform("base_footprint", 'enemy_closest', rospy.Time())
            trans = trans_stamped.transform
            # trans = self.tfBuffer.lookup_transform('enemy_closest', "base_footprint", rospy.Time(), rospy.Duration(4))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            # rate.sleep()
            # rospy.logwarn(e)
            return False, 0, 0
        # rospy.loginfo(trans)
        # rospy.loginfo(type(trans))
        
        dist = (trans.translation.x**2 + trans.translation.y**2)**0.5
        rad = atan2(trans.translation.y, trans.translation.x)
        # print ("trans.translation.x:{}, trans.translation.y:{}".format(trans.translation.x, trans.translation.y))

        # rot = trans.rotation
        # rad = tf.transformations.euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])[2]

        return True, dist, rad


if __name__ == '__main__':
    rospy.init_node('my_run')
    bot = RandomBot('myRun')
    bot.strategy()
