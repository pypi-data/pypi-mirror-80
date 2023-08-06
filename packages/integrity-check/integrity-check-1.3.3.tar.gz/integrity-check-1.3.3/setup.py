import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="integrity-check", 
    version="1.3.3",
    author="ArtFab",
    author_email="auz.tin@outlook.com",
    description="A replacement for assert",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArtFab/integrity-py",
    packages=["integrity_check"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
