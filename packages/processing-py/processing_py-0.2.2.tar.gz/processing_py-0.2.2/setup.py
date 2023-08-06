import setuptools
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('processing_py/processing')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="processing_py", 
    version="0.2.2",
    author="Faruk Hammoud",
    author_email="farukhammoud@student-cs.fr",
    description="Graphics Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FarukHammoud/processing_py",
    packages=setuptools.find_packages(),
	package_data={'': extra_files},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)