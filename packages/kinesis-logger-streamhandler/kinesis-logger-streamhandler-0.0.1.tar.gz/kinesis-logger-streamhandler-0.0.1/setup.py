import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kinesis-logger-streamhandler",
    version="0.0.1",
    author="Roman Dembitsky",
    author_email="romande@gmail.com",
    description="AWS Kinesis logger streamhandler with AWS Session Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deromka/kinesis-logger-streamhandler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)