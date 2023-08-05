from distutils.core import setup #如果没有需要先安装
setup(name='alsolib',  #打包后的包文件名
      version='1.2.20200921',  #版本
      description='爱搜库1.2.20200921，请使用python原版下载',
      author='asunc',
      author_email='asunc@asunc.cn',
      url='http://asunc.cn',
      py_modules=['alsolib\\alsoapi','alsolib\\alsolib','alsolib\\alsoxes'],  #与前面的新建文件名一致
)