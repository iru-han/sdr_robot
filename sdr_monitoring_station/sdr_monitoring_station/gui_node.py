import sys
import rclpy
import cv2
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

# 1단계에서 변환한 파일에서 UI 클래스 가져오기
from .gui_ui import Ui_Form 

class GUIClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("부기 관제 모니터 (Client)")

        # ROS 2 노드 생성
        self.node = rclpy.create_node('gui_client_node')
        
        # 비전 영상 구독
        self.subscription = self.node.create_subscription(
            CompressedImage,
            '/vision/processed/compressed',
            self.image_callback,
            10
        )

        # UI 이벤트 연결 (페이지 이동 등)
        self.init_signals()

        self.frame_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: rclpy.spin_once(self.node, timeout_sec=0))
        self.timer.start(33) # 약 30 FPS

    def init_signals(self):
        """UI 버튼들과 기능을 연결합니다."""
        # 페이지 전환 버튼 예시 (StackedWidget 제어)
        self.ui.btn_next.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.btn_pre_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btn_next_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btn_pre_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

    def image_callback(self, msg):
        self.frame_count += 1
        if self.frame_count % 2 != 0: return # 성능을 위한 프레임 스킵

        try:
            arr = np.frombuffer(msg.data, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None: return

            # BGR -> RGB 변환
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape
            bytes_per_line = ch * w
            qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # gui.ui에 정의된 face_label에 영상 표시
            # .ui 파일 기준 face_label의 크기는 211x331입니다.
            pixmap = QPixmap.fromImage(qimg).scaled(
                self.ui.face_label.width(), 
                self.ui.face_label.height(), 
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.ui.face_label.setPixmap(pixmap)
            
        except Exception as e:
            print(f"Image Error: {e}")

    def closeEvent(self, event):
        self.node.destroy_node()
        rclpy.shutdown()
        event.accept()

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    window = GUIClient()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()