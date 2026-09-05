from setuptools import find_packages, setup

package_name = 'idc_percept'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hyeonji',
    maintainer_email='yujh5537@gmail.com',
    description='YOLO 기반 이상 탐지, 마커 인식, 좌표 변환. SRD SR-F14~F19',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
