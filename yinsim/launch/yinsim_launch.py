from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='yinsim',
            executable='yinnode',
            name='custom_yinnode',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'shout': False}
            ]
        )
    ])