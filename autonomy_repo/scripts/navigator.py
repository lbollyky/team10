from asl_tb3_lib.navigation import BaseNavigator, TrajectoryPlan
from asl_tb3_lib.math_utils import wrap_angle
from asl_tb3_lib.tf_utils import quaternion_to_yaw
from asl_tb3_msgs.msg import TurtleBotControl, TurtleBotState
from rclpy.node import Node
import rclpy
import numpy as np
from scipy.interpolate import splev



class Navigator(BaseNavigator):
    def __init__(self):
        super().__init__("navigator")
        self.V_PREV_THRES = 0.0001
        self.kp = 2.0

    def compute_control_with_goal(self, current_state: TurtleBotState, desired_state: TurtleBotState) -> TurtleBotControl:
        error = wrap_angle(desired_state.theta - current_state.theta)
        control = TurtleBotControl()
        control.omega = self.kp * error
        return control

    def compute_trajectory_tracking_control(self, trajectory_plan: TrajectoryPlan) -> TurtleBotControl:
        # """
        # Inputs:
        #     x,y,th: Current state
        #     t: Current time
        # Outputs:
        #     V, om: Control actions
        # """

        # TrajectoryPlan(path=..., path_x_spline=..., path_y_spline=..., duration=...)

#         2. The desired states x_d, xd_d, xdd_d, y_d, yd_d, ydd_d need to be computed differently. Use
# scipy.interpolate.splev to sample from the spline parameters given by the TrajectoryPlan argument.


        x = trajectory_plan.
        x_d = splev(trajectory_plan.path_x_spline, der=0)
        xd_d = splev(trajectory_plan.path_x_spline, der=1)
        xdd_d = splev(trajectory_plan.path_x_spline, der=2)
        y_d = splev(trajectory_plan.path_y_spline, der=0)
        yd_d = splev(trajectory_plan.path_y_spline, der=1)
        ydd_d = splev(trajectory_plan.path_y_spline, der=2)
        t = self.get_clock().now().to_sec()

        dt = t - self.t_prev
        x_d, xd_d, xdd_d, y_d, yd_d, ydd_d = self.get_desired_state(t)

        ########## Code starts here ##########

        if dt > 1e-6:
            self.x_dot = (x - self.x_prev) / dt
            self.y_dot = (y - self.y_prev) / dt

        u_1 = xdd_d + self.kpx * (x_d - x) + self.kdx * (xd_d - self.x_dot)
        u_2 = ydd_d + self.kpy * (y_d - y) + self.kdy * (yd_d - self.y_dot)

        self.x_prev = x
        self.y_prev = y

        v_dot = np.cos(th) * u_1 + np.sin(th) * u_2
        V = self.V_prev + v_dot * dt

        if abs(V) < self.V_PREV_THRES:
            V = self.V_PREV_THRES
        om = -np.sin(th) * u_1 / V + np.cos(th) * u_2 / V

        ########## Code ends here ##########

        # apply control limits
        V = np.clip(V, -self.V_max, self.V_max)
        om = np.clip(om, -self.om_max, self.om_max)

        # save the commands that were applied and the time
        self.t_prev = t
        self.V_prev = V
        self.om_prev = om

        self.error += np.sqrt((x_d - x)**2 + (y_d - y)**2) * dt

        control = TurtleBotControl()
        control.V = V
        control.omega = om
        return control


if __name__ == "__main__":
    rclpy.init()
    navigator = Navigator()
    rclpy.spin(navigator)
    rclpy.shutdown()