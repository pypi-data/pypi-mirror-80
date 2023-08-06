# See description in CONTRIBUTING.md

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siasearch",
    version="0.0.6",
    author="Timofey Molchanov",
    author_email="timofey.molchanov@merantix.com",
    description="SDK for SiaSearch platform API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merantix/siasearch_python_sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "matplotlib", "scikit-image", "requests"],
    python_requires=">=3.6",
)
