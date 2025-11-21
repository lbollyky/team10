# import os
# from launch import LaunchDescription
# from launch.actions import TimerAction
# from launch_ros.actions import Node
# from ament_index_python.packages import get_package_share_directory


# def generate_launch_desc():
#    "This will be the launch file we can define for the autonomous exploration part earlier implemented"
#    "We need to ensure we are also running the simulator and navigatory to enable the full stack to run"


#    exploration_node = Node(package="", executable='exploration_node', name='exploration_node', output='screen', parameters=[{'use_sim_time': True,}])


#    # We also ened to have RVIZ here to visualize the robot in an online environment as it navigates around obstacles and enters known states that are unoccupied (as we define in the problem statement earlier; perhaps this could vary based on exploration heuristics)


#    rviz_config_directory = os.path.join(get_package_share_directory('nav2_bringup'), 'rviz', 'nav2_default_view.rviz')
#    rviz_node = Node(package='rviz2', executable='rviz2', name='rviz2', output='screen', arguments=['-d', rviz_config_directory], parameters=[{'use_sim_time': True,}])


#    delayed_explore_node=TimerAction(period=3.0, actions=[exploration_node])


#    launchdescription = LaunchDescription()
#    launchdescription.add_action(rviz_node)
#    launchdescription.add_action(delayed_explore_node)
#    return launchdescription




