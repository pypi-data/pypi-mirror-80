import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cs2tc",
    version=os.environ.get("TAG", "0.0.0"),
    author="Hank Doupe",
    author_email="henrymdoupe@gmail.com",
    description="Helper functions for converting Compute Studio parameters to a format compatible with Tax-Calculator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdoupe/cs2tc",
    packages=setuptools.find_packages(),
    install_requires=["paramtools"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
