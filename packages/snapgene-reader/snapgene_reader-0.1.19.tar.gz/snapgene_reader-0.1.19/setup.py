"""
setup.py
install snapgene_reader by pip
"""
from setuptools import setup, find_packages

setup(
    name="snapgene_reader",
    version="0.1.19",
    author="yishaluo",
    maintainer="EdinburghGenomeFoundry",
    description="Convert Snapgene *.dna files dict/json/biopython.",
    long_description=open("README.rst").read(),
    license="MIT",
    keywords="DNA sequence design format converter",
    packages=find_packages(),
    install_requires=["biopython", "xmltodict", "html2text"],
)
