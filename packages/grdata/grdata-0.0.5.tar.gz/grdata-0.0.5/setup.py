import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grdata",
    version="0.0.5",
    author="Zac Thiel",
    author_email="digitalservices@grcity.us",
    description="Package to process data using the City of Grand Rapids systems",
    long_description_content_type="text/markdown",
    url="https://github.com/GRInnovation/grdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)