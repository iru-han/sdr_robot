import rclpy, time, json
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class SdrMissionController(Node):
    def __init__(self):
        super().__init__('sdr_mission_controller')
        
        self.state = "ACT1_NAV2"
        self.munchi_step = 0 
        self.act2_start_time = None
        
        self.current_gesture = "none"
        self.current_expression = "none"
        
        # 구독
        self.create_subscription(String, '/vision_fast_data', self.vision_cb, 10)
        self.create_subscription(String, '/person/hand', self.hand_cb, 10)
        self.create_subscription(String, '/person/expression', self.exp_cb, 10)
        
        self.face_pub = self.create_publisher(String, '/face_lcd', 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 제어 통합 타이머 (10Hz)
        self.create_timer(0.1, self.drive_loop)
        
        self.get_logger().info("👑 [SDR] 부기 컨트롤러 가동 - 후퇴 로직 정밀 보정")

    def hand_cb(self, msg):
        try: self.current_gesture = json.loads(msg.data).get("gesture", "none")
        except: pass

    def exp_cb(self, msg):
        self.current_expression = msg.data

    def vision_cb(self, msg):
        data = msg.data.split(':')
        obj_type, cx = data[0], int(data[1]) if len(data) > 1 else 0
        
        # 🎬 1막에서 파란색 발견 시
        if self.state == "ACT1_NAV2" and obj_type == "BLUE":
            self.get_logger().warn("🚨 [이벤트] 장애물 발견! 알람 시퀀스 시작")
            self.state = "ACT1_ALARM"
            self.munchi_step = 0
            self.act2_start_time = time.time()
            self.send_face("surprised")

        # 🎬 2막 로직 (이제 vision_cb에서 속도를 직접 보내지 않음)
        elif self.state == "ACT2_TRACKING":
            self.current_cx = cx # 위치값만 저장
            self.current_obj = obj_type

    def drive_loop(self):
        t = Twist()

        if self.state == "ACT1_NAV2":
            t.linear.x = 0.08

        elif self.state == "ACT1_ALARM":
            self.munchi_step += 1
            if self.munchi_step <= 5: # 0.5초 멈춤
                t.linear.x = 0.0
            elif self.munchi_step <= 25: # 2.0초 강한 후퇴 (속도 -0.2로 상향)
                t.linear.x = -0.2 
                if self.munchi_step % 5 == 0: self.get_logger().info("⬅️ 후진 중...")
            elif self.munchi_step <= 45: # 2.0초 회전
                t.angular.z = 1.0 # 회전 속도는 조금 낮춤 (부드럽게)
                self.send_face("angry")
            else:
                self.get_logger().info("✅ 알람 종료, 주인님 찾기 모드")
                self.state = "ACT2_TRACKING"
                self.munchi_step = 0

        elif self.state == "ACT2_TRACKING":
            # 2막 이동 제어를 여기서 수행 (경합 방지)
            if hasattr(self, 'current_obj') and self.current_obj == "MASTER":
                # 시선 추적 로직 생략 (이미 구현됨)
                pass
            else:
                t.angular.z = 0.3 # 주인 없으면 살살 회전

        self.cmd_pub.publish(t)

    def send_face(self, cmd):
        self.face_pub.publish(String(data=cmd))

def main():
    rclpy.init(); rclpy.spin(SdrMissionController()); rclpy.shutdown()