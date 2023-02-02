from typing import Optional, Dict, List
from launch import SomeSubstitutionsType
from launch import LaunchContext
from launch import LaunchDescriptionEntity
from launch.action import Action
from launch.actions import SetLaunchConfiguration
from launch.utilities import normalize_to_list_of_substitutions
from launch.utilities import perform_substitutions
from moveit_configs_utils import MoveItConfigsBuilder

class LoadMoveitConfig(Action):
    def __init__(
        self,
        robot_name: SomeSubstitutionsType,
        package_name: SomeSubstitutionsType,
        mappings: Optional[Dict] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__robot_name = normalize_to_list_of_substitutions(robot_name)
        self.__package_name = normalize_to_list_of_substitutions(package_name)
        self.__mappings = mappings
        
    def execute(self, context: LaunchContext) -> Optional[List[LaunchDescriptionEntity]]:
        moveit_config_builder = MoveItConfigsBuilder(
            robot_name=perform_substitutions(context, self.__robot_name), 
            package_name=perform_substitutions(context, self.__package_name)
            )
        moveit_config_builder.robot_description(mappings=self.__mappings)
        moveit_config = moveit_config_builder.to_moveit_configs()
        
        # Add the moveit config to the launch context
        context.extend_locals({'moveit_config': moveit_config})
        
        #Create important launch configuration variables
        moveit_package_path = SetLaunchConfiguration(
            "moveit_package_path", 
            value=str(moveit_config.package_path))
        moveit_robot_description = SetLaunchConfiguration(
            "moveit_robot_description", 
            value=moveit_config.robot_description["robot_description"])
        moveit_robot_semantic_description = SetLaunchConfiguration(
            "moveit_robot_description_semantic", 
            value=str(moveit_config.robot_description_semantic["robot_description_semantic"]))
        moveit_ros2_controllers_file = SetLaunchConfiguration("moveit_ros2_controllers_file", value=str(moveit_config.package_path / "config/ros2_controllers.yaml"))
        return [moveit_package_path, moveit_robot_description, moveit_ros2_controllers_file, moveit_robot_semantic_description]