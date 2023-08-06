# -*- coding: utf-8 -*-
import setuptools, os


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="py-logging-logship",
    version= os.getenv('BUILD_BUILDNUMBER', 'dev'),
    description="Python logship logging handler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Andrey Maslov",
    author_email="info@logship.io",
    url="https://github.com/logship/py-logging-logship",
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires=">=3.6",
    install_requires=["rfc3339", "requests", "unpaddedbase64"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
