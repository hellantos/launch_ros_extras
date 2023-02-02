from setuptools import setup, find_packages

package_name = 'launch_ros_extras'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=["resource", "test"]),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Christoph Hellmann Santos',
    maintainer_email='ipa@ipa.de',
    description='Extra actions for ros2 launch system that are often used.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
