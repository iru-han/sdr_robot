import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'sdr_brain_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'models'), glob('models/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='study.iru@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'detect_human = sdr_brain_system.detect_human:main',
            'mission_controller = sdr_brain_system.sdr_mission_controller:main',
            'sdr_digit_reader = sdr_brain_system.sdr_digit_reader:main',
        ],
    },
)
