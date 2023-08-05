import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hlib",
    version="0.1.0",
    author="Hunter LaTourette",
    author_email="hlatourette@gmail.com",
    description="simple graph library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hlatourette/hlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)