import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pseanalytics",
    version="0.0.3",
    author="Kent Ballon",
    author_email="kentballon@gmail.com",
    description="stock trading api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kentballon/pseanalytics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 2.7',
)
