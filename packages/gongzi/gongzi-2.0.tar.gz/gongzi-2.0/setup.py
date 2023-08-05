#coding=utf-8
from distutils.core import setup

setup(
    name='gongzi',#发布模块名字，版本号，模块功能描述，作者名称，作者邮箱，发布的模块
    version='2.0',
    description='这是一个用于计算公司员工工资的计算方法',
    author='叶海陇',
    author_email='1003809568@qq.com',
    py_modules=['gongzi.Salary']
)

#然后在fabu右击鼠标打开终端 python setup.py sdist 回车建立一个dist里面压缩包就可以发布分享