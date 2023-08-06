import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rs-simtools",
    version="0.0.4",
    author="Gavin Bascom",
    author_email="gavin@redesignscience.com",
    description="OMMTK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedesignScience/RSSimTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)