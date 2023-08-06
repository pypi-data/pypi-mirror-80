from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="class-serializer",
    version="0.0.3",
    author="Aaron Mamparo",
    author_email="aaronmamparo@gmail.com",
    description="Serialize classes into JSON and vice-versa using simple annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amamparo/python-class-serializer",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.7",
)
