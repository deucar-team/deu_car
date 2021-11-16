#!/usr/bin/env python

import rospy
from smach import State
from bot_drive_controller import BotDrive
from std_msgs.msg import Bool, Float32
from sensor_msgs.msg import LaserScan
from scan_blocking_bar import ScanBar
# state : http://wiki.ros.org/smach/Tutorials/Getting%20Started
from bot_lane_tracker import BotLaneTracker

class BotReady(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.botDrive = BotDrive()
        
    def execute(self, ud):
        rospy.loginfo("Ready")
        rospy.sleep(rospy.Duration(3))
        return 'success'
        
class ScanBlockBar(State):
    # Scanning To Bloacking Bar
    # Drive Start or Stop
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.scan_blocking_bar = ScanBar()
        self.botDrive = BotDrive()
        self.rate = rospy.Rate(20)
        
    def execute(self, ud):
        current_time = int(rospy.Time.now().to_sec())
        target_time = current_time + 3
        rospy.loginfo("Blocking Bar is Opened")
        
        while target_time > int(rospy.Time.now().to_sec()):
            self.botDrive.set_linear(1)
            self.botDrive.set_angular(0)
            self.botDrive.bot_drive()
            return 'success'
            
class BotLaneTrack(State):
    # default Driving state
    # Scanning Event
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.left_line = BotLaneTracker('my_left_camera/rgb/image_raw')
        self.right_line = BotLaneTracker('my_right_camera/rgb/image_raw')
        self.botDrive = BotDrive()
        
        self.is_success = False

    def execute(self, ud):
        rospy.loginfo("Now Driving")
        while True:
            # Transition Start
            if self.is_success:
                return 'success'
            # Transition End

            cx = (self.left_line.cx + self.right_line.cx) / 2
            err = -float(cx) / 80
            if abs(err) > 0.14:
                self.botDrive.set_linear(0.4)
                self.botDrive.set_angular(err)
            elif abs(err) < 0.14:
                self.botDrive.set_linear(1)
                self.botDrive.set_angular(err)
            self.botDrive.bot_drive()