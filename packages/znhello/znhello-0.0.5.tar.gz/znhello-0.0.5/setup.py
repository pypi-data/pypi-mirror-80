# -*- coding: utf-8 -*-
# @Time    : 2020/9/22 下午3:29
# @Author  : jinzening
# @File    : setup.py
# @Software: PyCharm

from distutils.core import setup
import setuptools

setup(
    name='znhello',  # 包的名字
    version='0.0.5',  # 版本号
    description='project describe',  # 描述
    author='jinzening',  # 作者
    author_email="zening918@163.com",

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
