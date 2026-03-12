import rclpy
import cv2
import json
import os
import threading
import queue
import numpy as np
import time
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from ultralytics import YOLO
import mediapipe as mp
from ament_index_python.packages import get_package_share_directory
import math

class DetectHumanNode(Node):
    def __init__(self):
        super().__init__('detect_human_node')

        # YOLO 모델
        self.yolo_model = YOLO("yolov8n.pt")
        pkg_path = get_package_share_directory("sdr_brain_system")
        weights_path = os.path.join(pkg_path, "models", "best.pt")
        self.expression_model = YOLO(weights_path)

        # MediaPipe Hands
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)

        # Queue for thread-safe image processing
        self.img_queue = queue.Queue(maxsize=1)

        # Last log timestamps
        self.last_log_time = time.time()
        self.last_hand_log_time = time.time()

        self.label_map = {0: "anger", 1: "fear", 2: "happy", 3: "neutral", 4: "sad"}

        # ROS Subscriber & Publisher
        self.sub = self.create_subscription(
            CompressedImage, '/image_raw/compressed', self.image_callback, 10)
        self.hand_pub = self.create_publisher(String, '/person/hand', 10)
        self.exp_pub = self.create_publisher(String, '/person/expression', 10)

        # Start inference thread
        threading.Thread(target=self.inference_worker, daemon=True).start()

    def image_callback(self, msg):
        if self.img_queue.empty():
            self.img_queue.put(msg)

    # ---------------------------------------------
    # Helper: joint angle 계산
    def angle(self, a, b, c):
        ba = [a.x - b.x, a.y - b.y]
        bc = [c.x - b.x, c.y - b.y]
        dot = ba[0]*bc[0] + ba[1]*bc[1]
        norm_ba = math.sqrt(ba[0]**2 + ba[1]**2)
        norm_bc = math.sqrt(bc[0]**2 + bc[1]**2)
        if norm_ba * norm_bc == 0:
            return 0
        return math.degrees(math.acos(dot / (norm_ba * norm_bc)))

    # ---------------------------------------------
    # 손가락이 펴져있는지 판단
    def is_finger_straight(self, landmarks, tip_idx, pip_idx, mcp_idx):
        return self.angle(landmarks[tip_idx], landmarks[pip_idx], landmarks[mcp_idx]) > 160

    # ---------------------------------------------
    # 제스처 판단
    def get_gesture(self, hand_landmarks):
        landmarks = hand_landmarks.landmark

        idx_s = self.is_finger_straight(landmarks, 8, 6, 5)
        mid_s = self.is_finger_straight(landmarks, 12, 10, 9)
        rng_s = self.is_finger_straight(landmarks, 16, 14, 13)
        pnk_s = self.is_finger_straight(landmarks, 20, 18, 17)

        # 엄지 좌/우 손 모두 대응
        wrist_x = landmarks[0].x
        thm_tip = landmarks[4].x
        thm_mcp = landmarks[2].x
        thm_o = (thm_tip - wrist_x) * (thm_mcp - wrist_x) > 0

        if idx_s and not mid_s and not rng_s and not pnk_s:
            return "지시"
        if idx_s and mid_s and not rng_s and not pnk_s:
            return "브이"
        if idx_s and mid_s and rng_s and pnk_s:
            return "보"
        if not idx_s and not mid_s and not rng_s and not pnk_s and thm_o:
            return "엄지척"
        return "not known"

    # ---------------------------------------------
    # 손 인식 및 ROS 퍼블리시
    def detect_hand(self, image):
        res = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                gesture = self.get_gesture(hand_landmarks)

                current_time = time.time()
                if current_time - self.last_hand_log_time >= 5.0:
                    self.get_logger().info(f"Detected Gesture: {gesture}")
                    self.last_hand_log_time = current_time

                data = {"gesture": gesture, "tip_x": hand_landmarks.landmark[8].x}
                self.hand_pub.publish(String(data=json.dumps(data)))

    # ---------------------------------------------
    # 표정 인식 및 ROS 퍼블리시
    def detect_expression(self, image):
        res = self.expression_model(image)
        for r in res:
            for b in r.boxes:
                if float(b.conf[0]) < 0.4:
                    continue
                cls_idx = int(b.cls[0])
                conf = float(b.conf[0])
                current_time = time.time()
                if current_time - self.last_log_time >= 5.0:
                    label = self.label_map.get(cls_idx, "unknown")
                    self.get_logger().info(f"Detected Expression: {label} (conf: {conf:.2f})")
                    self.last_log_time = current_time

    # ---------------------------------------------
    # Inference thread
    def inference_worker(self):
        while rclpy.ok():
            try:
                msg = self.img_queue.get(timeout=1.0)
                np_arr = np.frombuffer(msg.data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                results = self.yolo_model(frame)

                # 가장 큰 사람 영역 선택
                max_area = 0
                best_crop = None
                for r in results:
                    for box in r.boxes:
                        if int(box.cls) == 0:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            area = (x2 - x1) * (y2 - y1)
                            if area > max_area:
                                max_area = area
                                best_crop = frame[y1:y2, x1:x2]

                if best_crop is not None and best_crop.size > 0:
                    self.detect_hand(best_crop)
                    self.detect_expression(best_crop)
            except queue.Empty:
                continue

# ---------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = DetectHumanNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()