import setuptools
import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
setuptools.setup(
  name="SPARQL-parser",
  version="0.0.2",
  author="njucsxh",
  author_email="csxianghuang@gmail.com",
  description="This is a SPARQL-parser, help you to get component of a SPARQL easily",
  long_description=read("README.rst"),
  long_description_content_type="text/markdown",
  url="https://github.com/cdhx/SPARQL-parse",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)