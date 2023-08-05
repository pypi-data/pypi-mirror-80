from distutils.core import setup

setup(
    name='yygq',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面没有方法，用于测试哦',  #描述
    author='sph', # 作者
    author_email='gaoqi110@163.com',
    py_modules=['dui.jiuzhe','dui.nijile'] # 要发布的模块
)
