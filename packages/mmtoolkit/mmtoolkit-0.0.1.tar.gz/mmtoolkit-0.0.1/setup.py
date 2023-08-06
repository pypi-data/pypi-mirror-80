from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='mmtoolkit',
      version='0.0.1',
      description='Microstructure-based Modelling Toolkit',
      url='https://gitee.com/weeshin/mmtoolkit',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Wang, Xin',
      author_email='xin.wang.418@aliyun.com',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.5, <4',
      install_requires=['matplotlib', 'numpy', 'tqdm'],
      zip_safe=False
      )