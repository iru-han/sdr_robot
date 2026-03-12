#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/compressed_image.hpp>
#include <std_msgs/msg/string.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/objdetect.hpp>

using namespace std::chrono_literals;

class BoogiVisionNode : public rclcpp::Node {
public:
    BoogiVisionNode() : Node("boogi_vision_node"), frame_count_(0) {
        // QoS 설정: 센서 데이터에 적합한 Best Effort 방식
        auto qos_profile = rclcpp::SensorDataQoS();

        image_sub_ = this->create_subscription<sensor_msgs::msg::CompressedImage>(
            "/image_raw/compressed", qos_profile,
            std::bind(&BoogiVisionNode::image_callback, this, std::placeholders::_1));
        
        // 뇌(Python)로 보낼 고속 데이터 퍼블리셔
        vision_pub_ = this->create_publisher<std_msgs::msg::String>("/vision_fast_data", 10);
        
        // GUI(Qt)로 보낼 전처리 영상 퍼블리셔
        processed_img_pub_ = this->create_publisher<sensor_msgs::msg::CompressedImage>("/vision/processed/compressed", 10);

        // 인식기 초기화
        hog_.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());
        if (face_cascade_.load("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")) {
            face_loaded_ = true;
        }
        
        clahe_ = cv::createCLAHE(2.0, cv::Size(8, 8));

        RCLCPP_INFO(this->get_logger(), "🚀 [C++] SDR perception system online - Ready for Mission!");
    }

private:
    void image_callback(const sensor_msgs::msg::CompressedImage::SharedPtr msg) {
        // 성능을 위해 2프레임마다 한 번 처리 (약 15fps)
        if (++frame_count_ % 2 != 0) return; 

        cv::Mat frame = cv::imdecode(cv::Mat(msg->data), cv::IMREAD_COLOR);
        if (frame.empty()) return;
        
        // 전처리 1: 연산 속도를 위해 320x240 리사이즈 (왜곡 방지)
        cv::resize(frame, frame, cv::Size(320, 240));

        // 전처리 2: 가우시안 블러로 자잘한 노이즈 제거
        cv::Mat blurred;
        cv::GaussianBlur(frame, blurred, cv::Size(5, 5), 0);

        std::string vision_msg = "NONE:0";

        // --- [STEP 1] 파란색 낙하물(장애물) 탐지 ---
        cv::Mat hsv, blue_mask;
        cv::cvtColor(blurred, hsv, cv::COLOR_BGR2HSV);
        // 파란색 범위 최적화 (실내 조명 고려)
        cv::inRange(hsv, cv::Scalar(100, 130, 50), cv::Scalar(130, 255, 255), blue_mask);
        
        // 모폴로지 연산으로 노이즈 제거
        cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5));
        cv::morphologyEx(blue_mask, blue_mask, cv::MORPH_OPEN, kernel);
        
        std::vector<std::vector<cv::Point>> contours;
        cv::findContours(blue_mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
        
        double max_area = 0;
        cv::Rect box_rect;
        for (const auto& cnt : contours) {
            double area = cv::contourArea(cnt);
            if (area > 2000 && area > max_area) { // 최소 면적 기준 2000
                max_area = area;
                box_rect = cv::boundingRect(cnt);
            }
        }

        if (max_area > 0) {
            int cx = box_rect.x + box_rect.width / 2;
            vision_msg = "BLUE:" + std::to_string(cx);
            // 시각화: 파란색 박스
            cv::rectangle(frame, box_rect, cv::Scalar(255, 0, 0), 2);
            cv::putText(frame, "OBSTACLE", box_rect.tl(), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255,0,0), 2);
        } 
        // --- [STEP 2] 상자가 없으면 사람(작업자) 탐지 ---
        else {
            cv::Point target_center(-1, -1);
            if (detect_master(blurred, target_center)) {
                vision_msg = "MASTER:" + std::to_string(target_center.x);
                // 시각화: 노란색 원 (시선 추적용 타겟)
                cv::circle(frame, target_center, 8, cv::Scalar(0, 255, 255), -1);
                cv::putText(frame, "MASTER", target_center + cv::Point(10, 0), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0,255,255), 2);
            }
        }

        // 뇌(Python)로 데이터 전송
        auto out_msg = std_msgs::msg::String();
        out_msg.data = vision_msg;
        vision_pub_->publish(out_msg);

        // GUI 관제용 영상 가공 (중앙 가이드선 추가)
        cv::line(frame, cv::Point(160, 0), cv::Point(160, 240), cv::Scalar(200, 200, 200), 1);
        
        // 압축 후 전송
        std::vector<uchar> buf;
        cv::imencode(".jpg", frame, buf);
        auto img_msg = sensor_msgs::msg::CompressedImage();
        img_msg.header.stamp = this->now();
        img_msg.format = "jpeg";
        img_msg.data = buf;
        processed_img_pub_->publish(img_msg);
    }

    bool detect_master(cv::Mat& frame, cv::Point& center) {
        cv::Mat gray;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        clahe_->apply(gray, gray);

        // 1순위: 얼굴 인식
        std::vector<cv::Rect> faces;
        if (face_loaded_) {
            face_cascade_.detectMultiScale(gray, faces, 1.1, 4, 0, cv::Size(40, 40));
        }

        if (!faces.empty()) {
            cv::Rect f = faces[0];
            center = cv::Point(f.x + f.width / 2, f.y + f.height / 2);
            cv::rectangle(frame, f, cv::Scalar(0, 255, 0), 2);
            return true;
        }

        // 2순위: 전신(몸통) 인식
        std::vector<cv::Rect> persons;
        hog_.detectMultiScale(frame, persons, 0, cv::Size(8,8), cv::Size(16,16), 1.05, 2);
        
        if (!persons.empty()) {
            cv::Rect p = persons[0];
            // 몸통의 상단 30% 지점을 시선 추적 포인트로 설정
            center = cv::Point(p.x + p.width / 2, p.y + p.height * 0.3);
            cv::rectangle(frame, p, cv::Scalar(255, 100, 0), 2);
            return true;
        }
        return false;
    }

    // 멤버 변수
    rclcpp::Subscription<sensor_msgs::msg::CompressedImage>::SharedPtr image_sub_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr vision_pub_;
    rclcpp::Publisher<sensor_msgs::msg::CompressedImage>::SharedPtr processed_img_pub_;

    cv::HOGDescriptor hog_;
    cv::CascadeClassifier face_cascade_;
    cv::Ptr<cv::CLAHE> clahe_;
    bool face_loaded_ = false;
    int frame_count_ = 0;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<BoogiVisionNode>());
    rclcpp::shutdown();
    return 0;
}