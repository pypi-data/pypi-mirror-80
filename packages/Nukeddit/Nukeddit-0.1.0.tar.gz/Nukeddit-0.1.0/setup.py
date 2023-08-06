"""Setup script for nukeddit.
"""
import setuptools

VERSION = "0.1.0"
DESCRIPTION = " Remove your comment history on Reddit"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Nukeddit",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/0x00cl/nukeddit",
    author="Tomas Gutierrez L.",
    author_email="0x00cl@example.com",
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: End Users/Desktop",
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 3"],
    license="FreeBSD License",
    packages=setuptools.find_packages(),
    install_requires=["arrow", "backports-abc", "praw>=5", "PyYAML", "requests", "six", "tornado"],
    package_data={"nukeddit": ["*.example"]},
    entry_points={
        "console_scripts": [
            "nukeddit=nukeddit.app:main"
        ]
    }
)
