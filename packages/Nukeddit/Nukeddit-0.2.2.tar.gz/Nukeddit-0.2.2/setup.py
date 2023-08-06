import setuptools
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Nukeddit",
    version=get_version("nukeddit/__init__.py"),
    description="Remove your comment history on Reddit.",
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
    install_requires=["arrow", "praw>=7", "requests", "prawcore", "pyyaml", "argparse", "appdirs"],
    package_data={"nukeddit": ["*.example"]},
    entry_points={
        "console_scripts": [
            "nukeddit=nukeddit.app:main"
        ]
    }
)
