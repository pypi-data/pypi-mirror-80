import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psython",  # Replace with your own username
    version="0.0.11",
    author="Doron Goldberg",
    author_email="doron.goldberg@gmail.com",
    description="A package for SPSS methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cxt9/psython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

