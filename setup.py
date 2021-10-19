from setuptools import setup, find_packages


PACKAGE = "robula-plus"
NAME = "robula-plus"
DESCRIPTION = "Python implementation of algorithm Robula+ for generate robust XPath"
AUTHOR = "Oleksandr Korovii"
AUTHOR_EMAIL = "zeusfsx@gmail.com"
URL = "https://github.com/ZeusFSX/robula-plus"
VERSION = '0.0.1'


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      url=URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license='BSD',
      packages=find_packages(exclude=["tests.*", "tests"]),
      install_requires=[
            "lxml~=4.6.2"
      ],
      zip_safe=False)
