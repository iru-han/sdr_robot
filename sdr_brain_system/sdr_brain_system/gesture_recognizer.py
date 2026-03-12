import numpy as np
import math
import time

class GestureRecognizer:
    def __init__(self):
        self.gesture_history = []
        self.last_state = "none"

    def calculate_angle(self, a, b, c):
        ba = np.array([a.x - b.x, a.y - b.y])
        bc = np.array([c.x - b.x, c.y - b.y])
        dot = np.dot(ba, bc)
        norm_ba = np.linalg.norm(ba)
        norm_bc = np.linalg.norm(bc)
        if norm_ba * norm_bc == 0: return 0
        return math.degrees(math.acos(max(-1.0, min(1.0, dot / (norm_ba * norm_bc)))))

    def is_straight(self, landmarks, tip, pip, mcp):
        return self.calculate_angle(landmarks[tip], landmarks[pip], landmarks[mcp]) > 160

    def recognize(self, hand_landmarks):
        l = hand_landmarks.landmark
        now = time.time()
        
        # 각 손가락 상태
        f1 = self.is_straight(l, 8, 6, 5)   # 검지
        f2 = self.is_straight(l, 12, 10, 9) # 중지
        f3 = self.is_straight(l, 16, 14, 13)# 약지
        f4 = self.is_straight(l, 20, 18, 17)# 새끼

        is_palm = f1 and f2 and f3 and f4
        is_fist = not f1 and not f2 and not f3 and not f4

        # 1. [쓰다듬기] 옆면 ^ 모양 판별
        side_dist = abs(l[5].x - l[17].x)
        is_side = side_dist < 0.04
        is_hook = (l[8].y > l[6].y and l[12].y > l[10].y)
        if is_side and is_hook: return "쓰다듬기"

        # 2. [이리와] 보 -> 주먹 -> 보 (1.5초 내 변화)
        curr = "fist" if is_fist else "palm" if is_palm else "none"
        if curr != self.last_state and curr != "none":
            self.gesture_history.append((curr, now))
            self.last_state = curr
        
        self.gesture_history = [h for h in self.gesture_history if now - h[1] < 1.5]
        h_states = [h[0] for h in self.gesture_history]
        
        if "palm" in h_states and "fist" in h_states and curr == "palm":
            return "이리와"

        if is_palm: return "보"
        if is_fist: return "주먹"
        if f1 and f2 and not f3 and not f4: return "브이"
        return "not known"