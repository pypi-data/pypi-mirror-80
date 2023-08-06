import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="seedoku",
    version="1.1",
    description="Play Sudoku with your Hands on a Real Time Camera Feed",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aashish2000/seedoku",
    author="Aashish",
    author_email="aash.ananth@gmail.com",
    license="GPL",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["seedoku"],
    include_package_data=True,
    install_requires=["tensorflow==2.3.0", "opencv-python==4.4.0.42","imutils==0.5.3"],
    entry_points={
        "console_scripts": [
            "seedoku=seedoku.__main__:main",
        ]
    },
)