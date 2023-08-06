import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lnrweb",
    version="1.0.0",
    description='A project for solving linear programming problem',
    author='Ashish Kumar',
    long_description=long_description,
    url='https://github.com/Ashish2000L/linear_programing',
    packages=setuptools.find_packages(),
    )
