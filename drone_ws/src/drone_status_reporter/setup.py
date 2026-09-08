from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'drone_status_reporter'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/drone_status_reporter']),
        ('share/drone_status_reporter', ['package.xml']),
        (os.path.join('share', 'drone_status_reporter', 'launch'),
            glob('launch/*.launch.py')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dhruv',
    maintainer_email='dhruv@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'monitor = drone_status_reporter.status_monitor:main',
            'commander = drone_status_reporter.offboard_commander:main',
            'mission1 = drone_status_reporter.task1:main',
	    'fake_odom = drone_status_reporter.fake_odom:main',
	    'path_tracer = drone_status_reporter.path_tracer:main',
        ],
    },
)
