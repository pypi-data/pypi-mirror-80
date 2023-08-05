from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="covidcountydata",
    version="0.8.0",
    description="Python client for accessing the COVID County Data database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CovidCountyData/covidcountydata.py",
    author="Valorum Data",
    author_email="info@valorumdata.com",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["covidcountydata"],
    python_requires=">=3.5, <4",
    install_requires=["requests", "pandas", "email_validator", "us", "urllib3"],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/CovidCountyData/covidcountydata.py/issues",
        "Source": "https://github.com/CovidCountyData/covidcountydata.py",
    },
)
