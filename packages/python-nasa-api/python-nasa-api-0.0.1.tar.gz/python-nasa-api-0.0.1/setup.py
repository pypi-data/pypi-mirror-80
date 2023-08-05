from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="python-nasa-api",
    version="0.0.1",
    description="Simple NASA Api @rapper written in Python!",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=['nasaapi'],
    keywords="python-nasa-api",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    license="MIT",
)