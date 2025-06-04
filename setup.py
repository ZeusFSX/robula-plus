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
            "lxml~=5.4"
      ],
      python_requires='>=3.12',
      classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.12',
      ],
      zip_safe=False)
