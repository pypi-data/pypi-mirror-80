import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TheAlgorithms-pkg-YOUR-USERNAME-HERE", # Replace with your own username
    version="0.0.2",
    author="Vireakpheakkdey Tiv",
    author_email="vtiv@deakin.edu.au",
    description="A sample package to demonstrate how the packaging work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tivpheakkdey/TheAlgoritms_pkg",
    download_url = "https://github.com/tivpheakkdey/TheAlgoritms_pkg/archive/0.0.3.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=[
          'string',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)