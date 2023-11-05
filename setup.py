#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="zmqdisplay",
    version="0.0.1",
    description="Client for displaying images sent over zmq.",
    author="Benjamin D. Killeen",
    author_email="killeen@jhu.edu",
    url="https://github.com/benjamindkilleen/zmqdisplay",
    install_requires=[
        "numpy",
        "click",
        "pyzmq",
        "rich",
        "opencv-python",
        "screeninfo",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "zmqdisplay = zmqdisplay.__main__:cli",
        ]
    },
)
