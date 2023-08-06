import sys
from os import path

from setuptools import setup, find_packages

from notetool.tool import get_version

version_path = path.join(path.abspath(
    path.dirname(__file__)), 'script/__version__.md')

version = get_version(sys.argv, version_path, step=32)

install_requires = []

setup(name='notebuild',
      version=version,
      description='notebuild',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',
      packages=find_packages(),
      entry_points={'console_scripts': [
          'notebuild = notebuild.core:notebuild', ]},
      install_requires=install_requires,
      )
