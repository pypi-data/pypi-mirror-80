import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numfracpy",
    version="0.1",
    author="Jorge Hernan Lopez, Alejandro Perez",
    author_email="jhlopezm2@gmail.com, aaappprrr@gmail.com",
    description="Package to perform calculations in fractional calculus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhlopezm/NUMFRACPY",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)