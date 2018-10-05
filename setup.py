#!/usr/bin/env python
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Author(s): Matthieu Coudron <matthieu.coudron@lip6.fr>
#

from setuptools import setup

# How to package ?
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#setup-py
# http://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies
# 
# if something fail during install, try running the script with sthg like
# DISTUTILS_DEBUG=1 python3.5 setup.py install --user -vvv
setup(name="i3dispatch",
      version="0.1",
      description="Use your window manager bindings seamlessly across applications",
      long_description=open('README.md', 'r', encoding='utf-8').read(),
      url="http://github.com/teto/i3-dispatch",
      license="GPL",
      author="Matthieu Coudron",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      keywords=["i3 neovim"],
      packages=["i3dispatch"],
      entry_points={
          "console_scripts": [
            # creates 2 system programs that can be called from PATH
            'i3dispatch = i3dispatch.i3dispatch:main',
          ]
      },
      # pandas should include matplotlib dependancy right ?
      install_requires=[
        'neovim',
        'psutil',
      ],
      zip_safe=True,
      )
