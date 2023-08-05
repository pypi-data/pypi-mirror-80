# 此文件用于发布时指定需要发布的模块,每次你想发布你写好的模块时,你就在这个文件指定，然后调用这个文件打包。

from distutils.core import setup

setup(

    name         = 'Example_module',              # 模块的总称(写上你需要打包的文件的name)
    version      = '1.0',                           # 模块的版本号
    description  = '这个模块可以打印一些东西',         # 模块描述（一般都是描述一些模块的大致功能）
    author       = 'xcc',                           # 作者的名字
    autuor_email = '945246001@qq.com',              # 作者的邮箱
    py_modules   = ['Example_module.amodule' ,'Example_module.bmodule']    #指定你需要打包的具体模块

)

# python setup.py sdist             #打包
# python setup.py install           #装包
# 可以建一个文件专门放下载下来的模块，然后在哪个文件里面安装就好了。




