from setuptools import find_packages, setup

from disturbia.version import VERSION

with open("README.md", encoding="utf-8") as readme_file:
    long_description = readme_file.read()


setup(
    name="disturbia",
    author="Khurram Raza",
    description="Library for set of simple methods regarding distribution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="ikhurramraza@gmail.com",
    url="https://github.com/ikhurramraza/disturbia",
    keywords="distribution sampling",
    license="MIT",
    classifiers=["License :: OSI Approved :: MIT License"],
    version=VERSION,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    python_requires=">=3.0, <4",
)
