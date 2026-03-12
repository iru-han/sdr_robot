import rclpy
import cv2
import numpy as np
import os
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from tensorflow import keras
from ament_index_python.packages import get_package_share_directory

class SdrDigitReaderNode(Node):
    def __init__(self):
        super().__init__('sdr_digit_reader')
        
        # 1. 모델 로드 (노트북에서 만든 모델 파일 경로)
        pkg_path = get_package_share_directory("sdr_brain_system")
        model_path = os.path.join(pkg_path, "models", "finetuned_digit_model.keras")
        self.model = keras.models.load_model(model_path)
        
        self.digit_pub = self.create_publisher(String, '/person/digit', 10)
        self.sub = self.create_subscription(CompressedImage, '/image_raw/compressed', self.image_callback, 10)

        self.current_mission_state = "ACT0_SLEEPY"
        self.create_subscription(String, '/mission_state', self.state_cb, 10)

        self.get_logger().info("🔢 Keras 기반 숫자 인식 노드 가동")

    def state_cb(self, msg):
        self.current_mission_state = msg.data
        print("self.current_mission_state : ", self.current_mission_state)

    # 노트북의 전처리 로직 이식
    def preprocess_digit(self, roi_img):
        offset = 5
        roi_clean = roi_img[offset:-offset, offset:-offset]
        gray = cv2.cvtColor(roi_clean, cv2.COLOR_BGR2GRAY)
        # gray = np.flip(gray, 1) # 필요시 반전
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        blur = cv2.GaussianBlur(enhanced, (5, 5), 3)
        binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 21, 5)
        kernel = np.ones((5, 5), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
        return processed

    # 노트북의 추출 로직 이식
    def extract_digits(self, processed_img):
        contours, _ = cv2.findContours(processed_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        digit_rects = []
        roi_h, roi_w = processed_img.shape
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if area < 300 or area > (roi_h * roi_w * 0.95): continue
            if w / float(h) > 3.0: continue
            digit_rects.append((x, y, w, h))
        
        digit_rects = sorted(digit_rects, key=lambda r: r[2]*r[3], reverse=True)[:1] # 가장 큰거 1개
        digit_images = []
        for x, y, w, h in digit_rects:
            padding = 15
            x1, y1 = max(0, x-padding), max(0, y-padding)
            x2, y2 = min(roi_w, x+w+padding), min(roi_h, y+h+padding)
            digit_crop = processed_img[y1:y2, x1:x2]
            resized = cv2.resize(digit_crop, (28, 28), interpolation=cv2.INTER_AREA)
            digit_images.append(resized)
        return digit_images

    def image_callback(self, msg):
        # ACT4 단계가 아니면 아무것도 하지 않음 (초록 사각형도 안 그려짐)
        if self.current_mission_state != "ACT4_DELIVERY":
            return
        
        np_arr = np.frombuffer(msg.data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # 중앙 ROI 추출 (노트북 설정값)
        h, w, _ = frame.shape
        size = 300
        x1, y1 = (w-size)//2, (h-size)//2
        roi = frame[y1:y1+size, x1:x1+size]

        processed = self.preprocess_digit(roi)
        digit_imgs = self.extract_digits(processed)

        for img in digit_imgs:
            input_data = (img / 255.0).reshape(1, 28, 28, 1)
            pred = self.model.predict(input_data, verbose=0)
            digit = np.argmax(pred)
            
            # 인식된 숫자 발행 (1, 3, 9 위주)
            self.digit_pub.publish(String(data=str(digit)))

def main():
    rclpy.init()
    rclpy.spin(SdrDigitReaderNode())
    rclpy.shutdown()