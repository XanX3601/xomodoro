from setuptools import setup, find_packages

setup(
    name="xomodoro",
    version="1.0.0",
    description="my pomodoro timer",
    author="Thomas Petiteau",
    author_email="thomas.petiteau@outlook.com",
    url="https://github.com/XanX3601/xomodoro",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["xomodoro=xomodoro.main:main"]
    },
    install_requires=[
        "rich_click==1.6.1"
    ]
)
