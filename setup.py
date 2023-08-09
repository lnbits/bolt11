from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), "README.md")) as f:
    long_description = f.read()


setup(
    name="bolt11",
    version="0.0.1",
    url="https://github.com/lnbits/bolt11",
    author="eillarra",
    author_email="eneko@illarra.com",
    license="MIT",
    description="A library for encoding and decoding BOLT11 payment requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="bitcoin lightning-network bolt11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    packages=["bolt11"],
    package_data={"bolt11": ["py.typed"]},
    python_requires=">=3.6",
    install_requires=[
        "base58",
        "bech32",
        "bitstring",
        "ecdsa",
        "typing-extensions; python_version<'3.8'",
    ],
    zip_safe=False,
)
