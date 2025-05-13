# here we write the code for project management
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "ML_OPS_PROJECT1",
    version="0.1",
    author = "Venu",
    packages= find_packages(),
    install_requirements = requirements
)