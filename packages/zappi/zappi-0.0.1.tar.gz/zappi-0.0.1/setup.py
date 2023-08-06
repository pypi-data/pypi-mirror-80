import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zappi",
    version="0.0.1",
    author="Andrei Bahizi",
    author_email="andrei@bahizi.com",
    description="Base Zappi Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bahizi/zappi",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
