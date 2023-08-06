import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvigi",
    version="0.0.1",
    author="Roch Schanen",
    author_email="r.schanen@lancaster.ac.uk",
    description="a PYthon Vitual Instrument Graphic Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RochSchanen/pyvigi_dev",
    # packages=setuptools.find_packages(),
    packages = ['pyvigi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # zip_safe = False,
    python_requires='>=3.8'
)
