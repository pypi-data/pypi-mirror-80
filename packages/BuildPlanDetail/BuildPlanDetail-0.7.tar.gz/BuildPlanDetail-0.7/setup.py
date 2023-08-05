import setuptools
from setuptools import setup

setup(
    name='BuildPlanDetail',# 需要打包的名字,即本模块要发布的名字
    version='v0.7',#版本getFile
    description='获取代码改动的文件和方法', # 简要描述
    packages=setuptools.find_packages(),   #  需要打包的模块
    author='houyan', # 作者名
    author_email='houyan@qiyi.com',   # 作者邮件
    url='https://github.com/vfrtgb158/email', # 项目地址,一般是代码托管的网站
    requires=['requests','pygerrit2','PyMySQL','multiprocess','threadpool'], # 依赖包,如果没有,可以不要
    license='MIT'
)