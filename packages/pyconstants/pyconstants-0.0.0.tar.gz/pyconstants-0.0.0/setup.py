from setuptools import setup, find_packages

f = open("README.md", "r")
README = f.read()
f.close()

setup(
    name="pyconstants",
    version="0.0.0",
    author="Aurotriz",
    author_email="aurotriz@protonmail.com",
    description="A package that brings constants to python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Aurotriz/pyconstants",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)