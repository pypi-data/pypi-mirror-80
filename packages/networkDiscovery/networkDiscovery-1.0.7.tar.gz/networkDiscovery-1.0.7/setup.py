"""Setup file for netdisco."""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="networkDiscovery",
    version="1.0.7",
    description="Discover devices on your local network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/GokGok/network-discovery.git",
    author="championchangpeng",
    author_email="championchangpeng@gmail.com",
    license="Apache License 2.0",
    install_requires=["requests>=2.0", "zeroconf>=0.27.1"],
    python_requires=">=3",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Home Automation",
        "Topic :: System :: Networking",
    ],
)
