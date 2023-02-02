import xacro
from ament_index_python import get_package_share_directory

from launch import SomeSubstitutionsType
from launch import LaunchContext
from launch import LaunchDescriptionEntity
from launch.action import Action
from launch.actions import SetLaunchConfiguration
from launch.utilities import normalize_to_list_of_substitutions
from launch.utilities import perform_substitutions
from pathlib import Path
from typing import Optional, Dict, List


class LoadXacro(Action):
    """Action that loads a xacro file from a package and sets the contents
    as a launch configuration.
    """
    def __init__(
        self,
        *,
        package: SomeSubstitutionsType,
        file: SomeSubstitutionsType,
        mappings: Optional[
            Dict[SomeSubstitutionsType, SomeSubstitutionsType]]=None,
        configuration_variable: SomeSubstitutionsType="robot_description",
        **kwargs
    ) -> None:
        """Creates a LoadXacro action.
        
        :param package: The name of the package that contains the xacro file.
        :type package: SomeSubstitutionsType
        :param file: The name of the xacro file to load, can be relative path to the packages share directory.
        :type file: SomeSubstitutionsType
        :param mappings: Some mappings to use when loading the xacro file, defaults to None
        :type mappings: Optional[ Dict[SomeSubstitutionsType, SomeSubstitutionsType]], optional
        :param configuration_variable: The configuration variable to store the contents of the xacro file in, defaults to "robot_description"
        :type configuration_variable: SomeSubstitutionsType, optional
        """
        super().__init__(**kwargs)
        self.__package = normalize_to_list_of_substitutions(package)
        self.__file = normalize_to_list_of_substitutions(file)
        self.__mappings = mappings
        self.__configuration_variable = normalize_to_list_of_substitutions(configuration_variable)

    def execute(self, context: LaunchContext) -> Optional[List[LaunchDescriptionEntity]]:
        package = perform_substitutions(context, self.__package)
        package_share_path = get_package_share_directory(package)
        file_name = perform_substitutions(context, self.__file)
        file_path = Path(package_share_path).joinpath(file_name)
        mappings = {}
        for key, value in self.__mappings.items():
            key = perform_substitutions(context, key)
            value = perform_substitutions(context, value)
            mappings[key] = value
        doc = xacro.process_file(str(file_path), mappings=mappings)
        return [SetLaunchConfiguration(self.__configuration_variable, doc.toxml())]