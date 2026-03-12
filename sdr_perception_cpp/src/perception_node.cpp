#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/compressed_image.hpp>
#include <std_msgs/msg/string.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/objdetect.hpp>

using namespace std::chrono_literals;

// =================================================================
// 1. Data Model: 감지 결과를 담는 구조체
// =================================================================
struct DetectionResult {
    bool success = false;
    std::string label = "NONE";
    cv::Point center = cv::Point(0, 0);
    cv::Rect rect;
};

// =================================================================
// 2. Vision Logic: 색상 감지기 클래스 (SRP 적용)
// =================================================================
class ColorDetector {
public:
    ColorDetector() {
        kernel_ = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5));
    }

    DetectionResult detect(const cv::Mat& hsv, cv::Mat& draw_frame, 
                           std::string label, cv::Scalar low, cv::Scalar high) {
        DetectionResult result;
        cv::Mat mask;
        cv::inRange(hsv, low, high, mask);
        cv::morphologyEx(mask, mask, cv::MORPH_OPEN, kernel_);

        std::vector<std::vector<cv::Point>> contours;
        cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        double max_area = 0;
        for (const auto& cnt : contours) {
            double area = cv::contourArea(cnt);
            if (area > 1500 && area > max_area) {
                max_area = area;
                result.rect = cv::boundingRect(cnt);
                result.success = true;
            }
        }

        if (result.success) {
            result.label = label;
            result.center = (result.rect.br() + result.rect.tl()) * 0.5;
            
            // 시각화 로직
            cv::Scalar color = (label == "YELLOW") ? cv::Scalar(0, 255, 255) : 
                               (label == "GREEN") ? cv::Scalar(0, 255, 0) : cv::Scalar(255, 0, 0);
            cv::rectangle(draw_frame, result.rect, color, 2);
            cv::putText(draw_frame, label, result.rect.tl(), cv::FONT_HERSHEY_SIMPLEX, 0.5, color, 2);
        }
        return result;
    }

private:
    cv::Mat kernel_;
};

// =================================================================
// 3. Vision Logic: 사람/얼굴 감지기 클래스 (SRP 적용)
// =================================================================
class HumanDetector {
public:
    HumanDetector() {
        hog_.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());
        face_cascade_.load("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml");
        clahe_ = cv::createCLAHE(2.0, cv::Size(8, 8));
    }

    DetectionResult detect(cv::Mat& frame) {
        DetectionResult result;
        cv::Mat gray;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        clahe_->apply(gray, gray);

        // 1. 얼굴 우선 탐지
        std::vector<cv::Rect> faces;
        face_cascade_.detectMultiScale(gray, faces, 1.1, 4, 0, cv::Size(40, 40));

        if (!faces.empty()) {
            result.success = true;
            result.label = "MASTER";
            result.rect = faces[0];
            result.center = (result.rect.br() + result.rect.tl()) * 0.5;
            cv::rectangle(frame, result.rect, cv::Scalar(0, 255, 0), 2);
            return result;
        }

        // 2. 전신 탐지
        std::vector<cv::Rect> persons;
        hog_.detectMultiScale(frame, persons, 0, cv::Size(8,8), cv::Size(16,16), 1.05, 2);
        if (!persons.empty()) {
            result.success = true;
            result.label = "MASTER";
            result.rect = persons[0];
            result.center = cv::Point(result.rect.x + result.rect.width/2, result.rect.y + result.rect.height*0.3);
            cv::rectangle(frame, result.rect, cv::Scalar(255, 100, 0), 2);
        }
        return result;
    }

private:
    cv::HOGDescriptor hog_;
    cv::CascadeClassifier face_cascade_;
    cv::Ptr<cv::CLAHE> clahe_;
};

// =================================================================
// 4. Controller: ROS 2 Perception Node (통합 및 통신)
// =================================================================
class PerceptionNode : public rclcpp::Node {
public:
    PerceptionNode() : Node("boogi_vision_node"), frame_count_(0) {
        // 컴포넌트 초기화 (Composition)
        color_detector_ = std::make_unique<ColorDetector>();
        human_detector_ = std::make_unique<HumanDetector>();

        auto qos = rclcpp::SensorDataQoS();
        img_sub_ = this->create_subscription<sensor_msgs::msg::CompressedImage>(
            "/image_raw/compressed", qos, std::bind(&PerceptionNode::image_callback, this, std::placeholders::_1));
        
        state_sub_ = this->create_subscription<std_msgs::msg::String>(
            "/mission_state", 10, [this](const std_msgs::msg::String::SharedPtr msg){ current_state_ = msg->data; });

        vision_pub_ = this->create_publisher<std_msgs::msg::String>("/vision_fast_data", 10);
        processed_img_pub_ = this->create_publisher<sensor_msgs::msg::CompressedImage>("/vision/processed/compressed", 10);

        current_state_ = "ACT0_SLEEPY";
        RCLCPP_INFO(this->get_logger(), "🚀 [C++] Clean Architecture Perception Node Online!");
    }

private:
    void image_callback(const sensor_msgs::msg::CompressedImage::SharedPtr msg) {
        if (++frame_count_ % 2 != 0) return;

        cv::Mat frame = cv::imdecode(cv::Mat(msg->data), cv::IMREAD_COLOR);
        if (frame.empty()) return;
        cv::resize(frame, frame, cv::Size(320, 240));

        DetectionResult final_result;
        cv::Mat hsv;
        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        // --- UML 상태 패턴에 따른 위임(Delegation) ---
        if (current_state_ == "ACT0_SLEEPY" || current_state_ == "ACT1_ALARM" || current_state_ == "ACT2_WAIT") {
            final_result = color_detector_->detect(hsv, frame, "BLUE", cv::Scalar(100, 130, 50), cv::Scalar(130, 255, 255));
        } 
        else if (current_state_ == "ACT3_AUTHENTICATE") {
            final_result = human_detector_->detect(frame);
        } 
        else if (current_state_ == "ACT5_PAYMENT") {
            // 우선순위: 노랑 -> 초록 -> 파랑
            final_result = color_detector_->detect(hsv, frame, "YELLOW", cv::Scalar(20, 100, 100), cv::Scalar(35, 255, 255));
            if (!final_result.success)
                final_result = color_detector_->detect(hsv, frame, "GREEN", cv::Scalar(40, 50, 50), cv::Scalar(80, 255, 255));
            if (!final_result.success)
                final_result = color_detector_->detect(hsv, frame, "BLUE", cv::Scalar(100, 130, 50), cv::Scalar(130, 255, 255));
        }

        // 결과 퍼블리싱
        publish_data(final_result);
        publish_image(frame);
    }

    void publish_data(const DetectionResult& res) {
        auto msg = std_msgs::msg::String();
        msg.data = res.label + ":" + std::to_string(res.center.x);
        vision_pub_->publish(msg);
    }

    void publish_image(cv::Mat& frame) {
        cv::line(frame, cv::Point(160, 0), cv::Point(160, 240), cv::Scalar(200, 200, 200), 1);
        std::vector<uchar> buf;
        cv::imencode(".jpg", frame, buf);
        auto img_msg = sensor_msgs::msg::CompressedImage();
        img_msg.header.stamp = this->now();
        img_msg.format = "jpeg";
        img_msg.data = buf;
        processed_img_pub_->publish(img_msg);
    }

    // ROS 2 통신 객체 및 컴포넌트
    std::unique_ptr<ColorDetector> color_detector_;
    std::unique_ptr<HumanDetector> human_detector_;
    
    rclcpp::Subscription<sensor_msgs::msg::CompressedImage>::SharedPtr img_sub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr state_sub_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr vision_pub_;
    rclcpp::Publisher<sensor_msgs::msg::CompressedImage>::SharedPtr processed_img_pub_;

    std::string current_state_;
    int frame_count_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PerceptionNode>());
    rclcpp::shutdown();
    return 0;
}