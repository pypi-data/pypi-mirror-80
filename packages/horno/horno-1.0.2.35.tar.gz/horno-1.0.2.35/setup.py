import setuptools

import horno

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=horno.name,
    version=horno.version,
    author="afs",
    author_email="author@example.com",
    description="Lo que el cuerpo necesita",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dateutil', 'bcrypt', 'passlib', 'unidecode', # 'lxml',
    ],                 
)