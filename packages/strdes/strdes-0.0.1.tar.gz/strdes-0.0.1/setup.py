import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strdes",
    version="0.0.1",
    author="tootal",
    author_email="tootal@yeah.net",
    description="A string encrypt and decrypt library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tootal/strdes",
    packages=['strdes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)