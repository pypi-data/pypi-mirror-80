import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymetalog",
    version="0.2.2",
    author="Colin Smith, Travis Jefferies, Isaac J. Faber",
    description="A python package that generates functions for the metalog distribution. The metalog distribution is a highly flexible probability distribution that can be used to model data without traditional parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tjefferies/pymetalog",
    install_requires=[
          'numpy',
          'scipy',
    ],
    download_url = 'https://github.com/tjefferies/pymetalog/archive/0.2.2.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)