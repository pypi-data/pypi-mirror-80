import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Hypyxel", 
    version="0.0.6",
    author="CraziiAce",
    author_email="teddyjraz@gmail.com",
    description="A python wrapper for the Hypixel API.\n## Usage:\n**Skyblock Stats**: `from hypy import skyblock`\n**Skyblock Stats**: `from hypy import skyblock`\n`get_endpoints` returns a dict of all functions and the associated endpoint",
    long_description="WIP",
    long_description_content_type="text/markdown",
    url="https://github.com/CraziiAce/HyPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
