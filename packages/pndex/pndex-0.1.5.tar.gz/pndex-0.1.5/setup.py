from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pndex",
    version="0.1.5",
    description="A Python package to manage all python files in a folder at once in console",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/adityadand/pndex",
    author="Aditya Dand",
    author_email="dandaditya@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    py_modules=["pndex"],
    package_dir={'':'src'},
    install_requires=['pyfiglet','importlib','pylint'],

)

