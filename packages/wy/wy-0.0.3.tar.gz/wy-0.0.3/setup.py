import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wy", 
    version="0.0.3",
    author="Korakot Chaovavanich",
    author_email="korakot@gmail.com",
    description="Convenient tools for WayScript",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/korakot/wy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
