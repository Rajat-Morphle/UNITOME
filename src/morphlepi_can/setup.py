from setuptools import setup
from glob import glob
import os

package_name = 'morphlepi_can'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch/'), glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='morphle',
    maintainer_email='morphle@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "commander = morphlepi_can.commander:main",
            "can_tx = morphlepi_can.can_tx:main",
            "frame_tx = morphlepi_can.frame_tx:main",
            "frame_rx = morphlepi_can.frame_rx:main",
            "response = morphlepi_can.response:main",
            "trajectory = morphlepi_can.trajectory:main"
        ],
    },
)
