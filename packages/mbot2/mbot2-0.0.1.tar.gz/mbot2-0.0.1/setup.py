# -*- coding: utf-8 -*
import os
from setuptools import setup

dirs = ['mbot2']
modules = ['mbot2']
for path,dir_list,file_list in os.walk("./mbot2"):
    for dir_name in dir_list:
        if dir_name.find("__")==-1 and dir_name.find("egg")==-1:
            dirs.append((path+"/"+dir_name).replace("/",".").replace("..",""))
    for file_name in file_list:
        if file_name.find(".py")!=-1 and file_name.find("__")==-1 and file_name.find(".pyc")==-1:
            modules.append((path+"."+file_name.replace(".py","")).replace("/",".").replace("..",""))
# print(dirs,modules)
setup(
    name='mbot2',
    version='0.0.1',
    author='makeblock',
    author_email='flashindream@gmail.com',
    url='https://makeblock.com',
    description=u'libraries for mbot2 platform',
    packages=dirs,
    py_modules=modules,
    install_requires=['pyserial'],
)
# setup.py
# global-include *.pyc
# global-exclude *.py