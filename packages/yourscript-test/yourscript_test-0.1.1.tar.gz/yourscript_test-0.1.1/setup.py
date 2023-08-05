#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : click_cli
@Time    : 2020/9/21 11:27
@Auth    : luozhongwen
@Email   : luozw@inhand.com.cn
@File    : setup.py
@IDE     : PyCharm
------------------------------------
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yourscript_test',
    version='0.1.1',
    author='chineseluo',
    author_email='848257135@qq.com',
    url='https://github.com/chineseluo/UI_auto_project',
    description='this is a upload pkg test',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['yourscript', 'myClickDemo'],
    install_requires=[
        'click',
    ],
    entry_points="""
    [console_scripts]
    yourscript=yourscript:cli
    """
)