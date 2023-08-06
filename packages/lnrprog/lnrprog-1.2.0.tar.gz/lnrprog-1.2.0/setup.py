import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lnrprog",
    version="1.2.0",
    description='A project for solving linear programming problem',
    author='Ashish Kumar',
    long_description=long_description,
    url='https://github.com/Ashish2000L/linear_programing',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.18.4',
        'matplotlib>=3.2.1'
    ]
    )
