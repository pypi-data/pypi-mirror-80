import codecs
import os
import sys

from setuptools import setup, find_packages

about = {}
with open(os.path.join(os.path.dirname(__file__), 'hktestpack', 'hktest', '__version__.py'), 'r') as f:
    exec(f.read(), about)

def read(fname):
	return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

long_des = read("README.rst")
    
platforms = ['linux/Windows']
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

install_requires = [
]
NAME="src"
PACKAGES = [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]    
setup(name='hktestpack',
      version=about["__version__"],
      description=about["__description__"],
      long_description=long_des,
      packages=find_packages(include=['hktestpack', 'hktestpack.*']),
      author=about["__author__"],
      author_email=about["__author_email__"],
      url="https://github.com/hekai000/gopl" ,
      license="Apache License, Version 2.0",
      platforms=platforms,
      classifiers=classifiers,
      zip_safe=False,
      install_requires=install_requires
      
      )   
      
      

  
