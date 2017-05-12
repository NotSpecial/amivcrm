"""Install amivcrm."""

from setuptools import setup

with open("README.rst", "r") as file:
    DESCRIPTION = file.read()

setup(
    name="amivcrm",
    version='0.1',
    author='Alexander Dietmüller',
    description="A simple connector to the AMIV SugarCRM",
    long_description=DESCRIPTION,
    packages=['amivcrm'],
    install_requires=['suds-jurko>=0.6']
)
