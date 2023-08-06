import setuptools
from shutil import copyfile

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="r2cloud",
    version="0.0.2",
    author="Lukáš Plevač",
    author_email="lukasplevac@gmail.com",
    description="python SDK for R2CLOUD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lukas0025/r2cloud-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[
        'httpx',
        'pyorbital'
    ],
)
