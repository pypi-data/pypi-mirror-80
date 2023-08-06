import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shreyansh.kushwaha", # Replace with your own username
    version="0.0.1",
    author="Shreyansh Kushwaha",
    author_email="shreyansh.halk@gmail.com",
    description="This python package will help you to perform various operations on 2 numbers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)