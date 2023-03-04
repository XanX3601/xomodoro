from setuptools import setup, find_packages

setup(
    name="xomodoro",
    version="1.0.0",
    description="my pomodoro timer",
    author="Thomas Petiteau",
    author_email="thomas.petiteau@outlook.com",
    url="https://github.com/XanX3601/xomodoro",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["xomodoro=xomodoro.main:main"]},
    install_requires=[
        "importlib_resources==5.12.0",
        "notify-py==0.3.42",
        "rich_click==1.6.1",
    ],
)
