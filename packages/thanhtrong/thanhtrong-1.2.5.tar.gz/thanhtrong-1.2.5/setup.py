from setuptools import setup
import setuptools
def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="thanhtrong",
    version="1.2.5",
    description="A Python package to get weather reports for any location.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tranthanhtrong/py",
    author="Tran Thanh Trong",
    author_email="trongttce130169@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    install_requires=["requests"],
)