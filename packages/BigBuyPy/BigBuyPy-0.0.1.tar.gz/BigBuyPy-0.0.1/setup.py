import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BigBuyPy", # Replace with your own username
    version="0.0.1",
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