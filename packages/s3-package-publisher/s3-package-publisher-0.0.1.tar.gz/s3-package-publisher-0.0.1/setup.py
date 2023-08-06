import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3-package-publisher",
    version="0.0.1",
    author="Aaron Mamparo",
    author_email="aaronmamparo@gmail.com",
    description="A command-line utility that publishes your python package to your own S3 repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amamparo/s3-package-publisher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
