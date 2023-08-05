#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time   : 2020/9/22 10:26 AM
# @Author : Dutt
# @Email  : dutengteng1@163.com
# @File   : setup.py.py

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "gagorastertiler",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "gagorastertiler","rastertile"),
    description = "An raster tiler tool",
    long_description = "An raster tiler tool, support geotedic projection and tianditu tile method",
    license = "MIT Licence",

    author = "dutengteng",
    author_email = "dutengteng1@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["gagoos"]          #这个项目需要的第三方库
)
