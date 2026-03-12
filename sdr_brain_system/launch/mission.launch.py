from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='sdr_perception_cpp', executable='perception_node', name='perception'),
        Node(package='sdr_brain_system', executable='detect_human', name='detect_human'),
        Node(package='sdr_brain_system', executable='mission_controller', name='mission_control'),
        Node(package='sdr_monitoring_station', executable='gui_node', name='monitoring')
    ])