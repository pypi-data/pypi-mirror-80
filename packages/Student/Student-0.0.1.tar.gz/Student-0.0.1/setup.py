import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Student", # Replace with your own username
    version="0.0.1",
    author= "sagar gajul",
    author_email="gajulsagar41@gmail.com",
    description="student information package",
    long_description=long_description,
    long_description_content_type="text/markdown",
   # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)