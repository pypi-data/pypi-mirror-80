# -*- coding: utf-8 -*-
# @Author  : jinzening/jingpengu
# @File    : setup.py
# @Software: PyCharm

from distutils.core import setup
import setuptools

setup(
    name='ZnPyobject',  # 包的名字
    version='0.0.1',  # 版本号
    description='项目的封装和简单继承',  # 描述
    author='靳泽宁 景鹏宇',  # 作者

    packages=setuptools.find_packages(),  # 包内需要引用的文件夹

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
