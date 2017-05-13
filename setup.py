"""Install amivcrm."""

from setuptools import setup

with open("README.rst", "r") as file:
    DESCRIPTION = file.read()

setup(
    name="amivcrm",
    version='0.3',
    author='Alexander Dietmüller',
    description="A simple connector to the AMIV SugarCRM",
    long_description=DESCRIPTION,
    packages=['amivcrm'],
    install_requires=['suds-jurko>=0.6'],
    url="https://github.com/NotSpecial/amivcrm",
    download_url="https://github.com/NotSpecial/amivcrm/releases/tag/0.3"
)
