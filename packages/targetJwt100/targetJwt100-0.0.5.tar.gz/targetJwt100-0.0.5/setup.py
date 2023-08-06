#  ! / user/ bin/ python
#  -*-  coding utf-8 -*-
# author : entang   
# time : 2020/9/24

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="targetJwt100",
  version="0.0.5",
  author="Example Author",
  author_email="author@example.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3.7",
  "License :: OSI Approved :: MIT License",
  ],
)