# coding=utf-8

"""
    @header setup.py
    @abstract   
    
    @MyBlog: http://www.kuture.com.cn
    @author  Created by Kuture on 2020/9/22
    @version 0.1.0 2020/9/22 Creation()
    @e-mail austinkuture@126.com
    
    @Copyright © 2020年 Mr.Li All rights reserved
"""


from setuptools import setup, find_packages

setup(
    name = "akbase2233",
    version = "0.1.0",
    keywords = ("pip", "akbase2233", "base", "timetool", "kuture", "encrypt", "decrypt", "base2233", "akbase"),
    description = "use you self password table, encrypt and decrypt you content",
    long_description = "akbase2233 主要用于使用自己的字母表进行，内容的加密与解密，其中最主要的特点是可以加密结果不是唯一的。\n"
                       "同样的内容加密后的结果却有所差异，但是却不影响正常的解密，所以其安全性相对有一定的提升。关键是可以设计属于\n"
                       "私有的密码表，不密码表不公开的情况，大大增加了破解的难度（其实是很难破解，概率极低）",
    license = "MIT Licence",

    url = "",
    author = "Kuture",
    author_email = "kuture@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['pickle', 'base64', 'random']
)