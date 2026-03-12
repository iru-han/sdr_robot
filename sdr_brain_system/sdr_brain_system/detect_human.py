import rclpy, cv2, json, os, threading, queue, numpy as np, time
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from ultralytics import YOLO
import mediapipe as mp
from ament_index_python.packages import get_package_share_directory
from .gesture_recognizer import GestureRecognizer # 분리한 파일 임포트

class DetectHumanNode(Node):
    def __init__(self):
        super().__init__('detect_human_node')
        
        # 모델 로드
        pkg_path = get_package_share_directory("sdr_brain_system")
        self.host_model = YOLO(os.path.join(pkg_path, "models", "hostface.pt"))
        self.expression_model = YOLO(os.path.join(pkg_path, "models", "best.pt"))
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.recognizer = GestureRecognizer()

        self.current_state = "ACT0_SLEEPY"
        self.img_queue = queue.Queue(maxsize=1)

        # 구독 및 발행
        self.create_subscription(String, '/mission_state', self.state_cb, 10)
        self.create_subscription(CompressedImage, '/image_raw/compressed', self.img_cb, 10)
        
        self.hand_pub = self.create_publisher(String, '/person/hand', 10)
        self.exp_pub = self.create_publisher(String, '/person/expression', 10)
        self.face_id_pub = self.create_publisher(String, '/person/face_id', 10)

        threading.Thread(target=self.inference_worker, daemon=True).start()

    def state_cb(self, msg): self.current_state = msg.data
    def img_cb(self, msg):
        if self.img_queue.empty(): self.img_queue.put(msg)

    def inference_worker(self):
        while rclpy.ok():
            # 💤 최적화: 특정 상태가 아니면 아예 연산을 하지 않음
            active_states = ["ACT3_AUTHENTICATE", "ACT5_PAYMENT"]
            if self.current_state not in active_states:
                time.sleep(0.5) # 쉬어감
                continue

            try:
                msg = self.img_queue.get(timeout=1.0)
                frame = cv2.imdecode(np.frombuffer(msg.data, np.uint8), cv2.IMREAD_COLOR)
                
                # 1. 주인 인증 단계 (얼굴 + 이리와 제스처 필요)
                if self.current_state == "ACT3_AUTHENTICATE":
                    # 얼굴 인식
                    res = self.host_model(frame, verbose=False)
                    for r in res:
                        for b in r.boxes:
                            if self.host_model.names[int(b.cls)] == "manager" and float(b.conf) > 0.6:
                                self.face_id_pub.publish(String(data="manager"))
                    
                    # 손 인식 (이리와)
                    self.process_hands(frame)

                # 2. 결제 단계 (쓰다듬기 필요)
                elif self.current_state == "ACT5_PAYMENT":
                    self.process_hands(frame)
                    # 표정도 같이 확인
                    self.process_expressions(frame)

            except: continue

    def process_hands(self, frame):
        res = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if res.multi_hand_landmarks:
            gesture = self.recognizer.recognize(res.multi_hand_landmarks[0])
            self.hand_pub.publish(String(data=json.dumps({"gesture": gesture})))

    def process_expressions(self, frame):
        res = self.expression_model(frame, verbose=False)
        for r in res:
            if r.boxes:
                label = {0:"anger", 1:"fear", 2:"happy", 3:"neutral", 4:"sad"}.get(int(r.boxes[0].cls), "unknown")
                self.exp_pub.publish(String(data=json.dumps({"expression": label})))

def main():
    rclpy.init(); rclpy.spin(DetectHumanNode()); rclpy.shutdown()