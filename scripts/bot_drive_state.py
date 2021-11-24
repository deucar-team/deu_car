#!/usr/bin/env python

import rospy
from smach import State
from bot_drive_controller import BotDrive
from std_msgs.msg import Bool, Float32
from sensor_msgs.msg import LaserScan
from scan_blocking_bar import ScanBar
# state : http://wiki.ros.org/smach/Tutorials/Getting%20Started
from bot_lane_tracker import BotLaneTracker
from scan_stop_line import ScanStopLine

class BotReady(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.botDrive = BotDrive()
        
    def execute(self, ud):
        rospy.loginfo("Ready? Wait for 3 seconds.")
        rospy.sleep(rospy.Duration(3))
        return 'success'
        
        
class ScannedBar(State):
    # Scanning To Blocking Bar
    # Drive Start or Stop
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.scan_blocking_bar = ScanBar()
        self.botDrive = BotDrive()
        self.rate = rospy.Rate(20)
        
    def execute(self, ud):
        time_now = int(rospy.Time.now().to_sec())
        target_time = time_now + 30

        while target_time > int(rospy.Time.now().to_sec()):
            if (self.scan_blocking_bar.result == True):
                rospy.loginfo("Blocking bar part is finished")
                return 'success'


            
class BotLaneTrack(State):
    # default Driving state
    # Scanning Event
    def __init__(self):
        State.__init__(self, outcomes=['success', 'scan_stop_line'])
        self.botDrive = BotDrive()
        
        self.scan_stop_line = ScanStopLine()
        self.is_stop_line = rospy.Subscriber('detect/is_stop_line', Bool, self.stop_line_callback)
        
        self.is_success = False
        self.is_stop_line = False
        
    def stop_line_callback(self, msg):
        if msg.data:
            self.is_stop_line = True
        else:
            self.is_stop_line = False

    def execute(self, ud):
        self.left_line = BotLaneTracker('my_left_camera/rgb/image_raw')
        self.right_line = BotLaneTracker('my_right_camera/rgb/image_raw')  # changed
        rospy.loginfo("Now Driving")
        while True:
            # Transition Start
            if self.is_stop_line:
                return 'scan_stop_line'
            if self.is_success:
                return 'success'
            # Transition End

            cx = (self.left_line.cx + self.right_line.cx) / 2
            err = -float(cx) / 80
            
            if abs(err) > 0.14:
                self.botDrive.set_linear(0.4)
                self.botDrive.set_angular(err)
            elif abs(err) < 0.14:
                self.botDrive.set_linear(1.0)
                self.botDrive.set_angular(err)
            self.botDrive.bot_drive()
            
            
class ScannedStopLine(State):
    # Scanning To Stop Line
    # Drive Start or Stop
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.botDrive = BotDrive()
        self.stop_line_sub = rospy.Subscriber('detect/stop_line_cx', Float32, self.stop_line_callback)
        self.rate = rospy.Rate(20)
        self.count = 0
        
    def stop_line_callback(self, msg):
        self.cs = msg.data
        
    def execute(self, ud):
        rospy.loginfo("Stop Line Scanned")
        time_now = int(rospy.Time.now().to_sec())
        target_time = time_now + 3  # 3 second wait
        
        while target_time > int(rospy.Time.now().to_sec()):
            self.botDrive.set_linear(0)
            self.rate.sleep()
        return 'success'
