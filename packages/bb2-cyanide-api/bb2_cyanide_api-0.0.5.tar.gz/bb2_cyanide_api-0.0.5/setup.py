import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bb2_cyanide_api",
    version="0.0.5",
    author="Tomas Trnecka",
    author_email="trnecka@gmail.com",
    description="Cyanide BB2 API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ttrnecka/bb2_cyanide_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)