#-*- coding:utf-8 -*-
import setuptools

#############################################
# File Name: setup.py
# Author: Yu Yuanjian
# Mail: yyjlaw@foxmail.com
# Created Time: 2020-9-24 11:36:30
#############################################

setuptools.setup(
    name="files2tree",
    version="0.1.1",
    author="Yu Yuanjian",
    author_email="yyjlaw@foxmail.com",
    description="make file directory to 2 dynamic tree-picture html,由虞元坚律师创作",
    long_description='make file directory to a treelist html file',
    long_description_content_type="text/markdown",
    # url="https://github.com/pythonml/douyin_image",
    packages=setuptools.find_packages(),
    install_requires=['pyecharts==1.8.1'],
    # entry_points={
    #     'console_scripts': [
    #         'files2tree=files2tree:main'
    #     ],
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)