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
    version = "0.1.1",
    keywords = ("pip", "akbase2233", "base", "timetool", "kuture", "encrypt", "decrypt", "base2233", "akbase"),
    description = "use you self password table, encrypt and decrypt you content",
    long_description = "akbase2233 可以使用自己的密码表进行内容的加密与解密，其中最主要的特点是加密结果不是唯一的。\n"
                       "虽然同样的内容加密后的结果有所差异，但是却不影响正常的解密，所以其安全性有很大的提升。关键是可以设计\n"
                       "私有的密码表，密码表不公开的情况下，基本上是不可解的。",
    license = "MIT Licence",

    url = "",
    author = "Kuture",
    author_email = "kuture@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['base64']
)