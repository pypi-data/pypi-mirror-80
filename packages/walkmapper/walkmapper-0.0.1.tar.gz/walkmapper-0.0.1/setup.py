import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="walkmapper",
    version="0.0.1",
    author="Sam Olson",
    author_email="solson1014@gmail.com",
    description="A package for plotting and animating .gpx files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam-olson/walkmapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
