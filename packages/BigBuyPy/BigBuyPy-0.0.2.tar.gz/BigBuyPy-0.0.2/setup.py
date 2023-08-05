import setuptools
import re
import os.path as op

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("BigBuyPy/__init__.py", "r") as fh:
    version_file = fh.read()

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    version_file,
                    re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

print(version)

setuptools.setup(
    name="BigBuyPy",  # Replace with your own username
    version=version,
    author="André Páscoa",
    author_email="andre@pascoa.org",
    description="Big Buy connector for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devandrepascoa/BigBuyPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
