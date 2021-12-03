#!/usr/bin/env python
# coding=utf-8

import rospy, cv2, numpy
from sensor_msgs.msg import Image
from std_msgs.msg import Bool, Float32
from scan_default import ScanDefault


class ScanStopLine(ScanDefault):
    def __init__(self):
        super(ScanStopLine, self).__init__()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.image_pub = rospy.Publisher('detect/stop_line', Image, queue_size=1)
        self.scan_stop_line = rospy.Publisher('detect/is_stop_line', Bool, queue_size=1)
        self.stop_line_cx_pub = rospy.Publisher('detect/stop_line_cx', Float32, queue_size=1)
        self.x = 0
        self.w = 0
        self.area = 0

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_white = numpy.array([0, 0, 200])
        upper_white = numpy.array([0, 0, 255])
        # lower_white = numpy.array([0, 0, 90])
        # upper_white = numpy.array([5, 5, 110])
        mask = cv2.inRange(hsv, lower_white, upper_white)

        h, w = mask.shape

        # mask[0: h / 2, 0: w] = 0
        # mask[h - (h / 8):h, 0:w] = 0
        # mask[0:h, 0:w / 4] = 0
        # mask[0:h, w - (w / 4):w] = 0

        # mask[0: h - (h / 4), 0: w] = 0
        # mask[0:h, 0:w / 4] = 0
        # mask[0:h, w - (w / 5):w] = 0

        mask[0: h - (h / 4), 0: w] = 0
        mask[0:h, 0:w / 4] = 0
        mask[0:h, w - (w / 8):w] = 0

        ret, thr = cv2.threshold(mask, 127, 255, 0)
        _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # print(self.area)
            if len(contours) <= 0:
                return  # not found

            cnt = contours[0]
            self.area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            mask = cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), 2)

            if self.area > 10000:
                self.scan_stop_line.publish(True)
                # image = cv2.circle(image, (self.x + self.w / 2, y + h / 2), 20, (0, 255, 0), -1)
                # image = self.bridge.cv2_to_imgmsg(image, 'bgr8')
                # self.image_pub.publish(image)

            else:
                self.scan_stop_line.publish(False)
                # self.stop_line_cx_pub.publish(self.x + self.w / 2)  # adjust stop line
                # print "stop line scanned"

            cv2.drawContours(mask, [cnt], 0, (255, 255, 0), 1)

            """
            cnt = contours[len(contours) - 1]
            area = max(list(map(lambda x: cv2.contourArea(x), contours))) # contour array max
            self.x, y, self.w, h = cv2.boundingRect(cnt)
            mask = cv2.rectangle(mask, (self.x, y), (self.x + self.w, y + h), (0, 0, 255), 2)
            cv2.drawContours(mask, [cnt], 0, (255, 255, 0), 1)
            # print area

            if 10000.0 < area:
                self.scan_stop_line.publish(True)
                self.stop_line_cx_pub.publish(self.x + self.w / 2)  # adjust stop line
                #print "stop line scanned"

            self.scan_stop_line.publish(False)
            image = cv2.circle(image, (self.x + self.w / 2, y + h / 2), 20, (0, 255, 0), -1)
            image = self.bridge.cv2_to_imgmsg(image, 'bgr8')
            self.image_pub.publish(image)
            """


if __name__ == "__main__":
    rospy.init_node('stop_line_finder')
    scan_stop_line = ScanStopLine()
    while not rospy.is_shutdown():
        scan_stop_line.rate.sleep()
        # print scan_stop_line.x