import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup

from std_msgs.msg import String

from yinyang_msgs.srv import Pipi


class Yin(Node):
    
    def __init__(self):
        super().__init__('yin')
        
        client_cb_group = None
        timer_cb_group = None
        self.srv = self.create_service(Pipi, 'yin_service', self.srv_callback)
        self.cli = self.create_client(Pipi, 'yang_service', callback_group=client_cb_group)
        self.call_timer = self.create_timer(1, self._timer_cb, callback_group=timer_cb_group)

        self.publisher_ = self.create_publisher(String, 'conversation', 10)
        
        
        self.req = Pipi.Request()
        self.count = 0
        self.str = [
            "I am Yin, some mistake me for an actual material entity but I am more of a concept",
            "Interesting Yang, so one could say, in a philosophical sense, we are two polar elements",
            "We, Yang, are therefore the balancing powers in the universe.",
            "Difficult and easy complete each other.",
            "Long and short show each other.",
            "Noise and sound harmonize each other.",
            "You shine your light."
        ]
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting...')

        self.time_to_send = True

    def _timer_cb(self):
        # self.get_logger().info('timer')
        if(self.time_to_send and self.count < len(self.str)):
            self.req.a = self.str[self.count]
            self.req.len = len(self.str[self.count])
            self.count +=1
            _ = self.cli.call_async(self.req)
            self.get_logger().info('request sent')
            self.time_to_send = False


    def srv_callback(self, req, res):
        self.get_logger().info(req.a)
        msg = String()
        s = 'Yang said: '+ req.a + ', ' + str(req.len)
        sum = 0
        for word in req.a:
            for ch in word:
                sum += ord(ch)
        s = s + ', ' + str(sum)
                
        msg.data = s
        self.publisher_.publish(msg)
        res.checksum = sum
        self.time_to_send = True
        # self.send_req(self.str[self.count])
        return res


def main(args=None):
    rclpy.init(args=args)
    yin = Yin()

    executor = MultiThreadedExecutor()
    executor.add_node(yin)
    executor.spin()
    yin.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
