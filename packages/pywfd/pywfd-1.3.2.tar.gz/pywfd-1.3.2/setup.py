from setuptools import setup, find_packages

setup(
    name="pywfd",
    version="1.3.2",
    description="A library to handle wfd files in python.",
    install_requires=["numpy", "dlchord"],
    author="anime-song",
    url="https://github.com/anime-song/wfdload",
    license="MIT",
    packages=["pywfd"],
)
