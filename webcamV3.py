import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        # Publisher für Farbbild
        self.publisher_color = self.create_publisher(Image, 'image_raw', 10)
        # NEU: Publisher für Graustufenbild
        self.publisher_gray = self.create_publisher(Image, 'image_gray', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.cap = cv2.VideoCapture(2)  # Kamera-Index anpassen
        self.bridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            # Farbbild publizieren (wie bisher)
            msg_color = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
            self.publisher_color.publish(msg_color)
            
            # NEU: Graustufenbild erstellen und publizieren
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            msg_gray = self.bridge.cv2_to_imgmsg(gray_frame, 'mono8')
            self.publisher_gray.publish(msg_gray)

def main():
    rclpy.init()
    node = CameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
