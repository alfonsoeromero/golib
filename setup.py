import os
from setuptools import setup, find_packages

root_dir_path = os.path.dirname(os.path.abspath(__file__))

long_description = open(os.path.join(root_dir_path, "README.md")).read()

setup(
    name="golib",
    version="0.0.1",
    author="Alfonso E. Romero",
    author_email="alfonsoeromero@gmail.com",
    description="A library for working with the Gene Ontology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[],
    license="MIT",
    keywords="gene ontology annotation protein bioinformatics",
    url="https://github.com/alfonsoeromero/golib",
    packages=find_packages(),
    data_files=[],
    include_package_data=True,
    scripts=[]
)
