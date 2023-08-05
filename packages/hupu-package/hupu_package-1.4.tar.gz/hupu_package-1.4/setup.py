# coding:utf-8

from setuptools import setup, find_packages
# or
# from distutils.core import setup

setup(
        name='hupu_package',     # 包名字
        version='1.4',   # 包版本
        description='Upload file to oss',   # 简单描述
        author='daizhanglong',  # 作者
        author_email='daizhanglong@hupu.com',  # 作者邮箱
        url='https://www.hupu.com',      # 包的主页
        license='MIT',
        packages=find_packages()              # 包
)