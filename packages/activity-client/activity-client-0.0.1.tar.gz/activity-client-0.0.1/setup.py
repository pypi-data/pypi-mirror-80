from setuptools import find_packages
from setuptools import setup

setup(
    name='activity-client',
    version='0.0.1',
    author='mingl_wang',
    author_email='wangminglu_1908@163.com',
    description='cloud activity API client library.',
    packages=find_packages(),
    install_requires=[
        'requests',
        'retrylib>=1.2.5',
    ],
)
