import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mnrva",
    version="0.0.8",
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
    install_requires=[
        'certifi==2019.11.28',
        'elasticsearch==7.5.1',
        'PyMySQL==0.9.3',
        'redis==3.4.1',
        'urllib3==1.24.3'
    ],
    python_requires='>=3.7',
)
