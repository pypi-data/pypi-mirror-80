import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mnrva",
    version="0.0.7",
    author="Brian Salazar",
    author_email="brian@mnrva.io",
    description="Minerva Libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mnrva.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)