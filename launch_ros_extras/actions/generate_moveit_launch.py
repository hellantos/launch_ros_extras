from typing import Callable, Optional, List
from launch import LaunchContext, LaunchDescriptionEntity
from launch.action import Action


class GenerateMoveitLaunch(Action):
    def __init__(self, *, function:Callable, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__function = function
    
    def execute(self, context: LaunchContext) -> Optional[List[LaunchDescriptionEntity]]:
        return [self.__function(context.get_locals_as_dict()["moveit_config"])]