import setuptools

with open("README.md", "r") as fha:
    long_description = fha.read()

setuptools.setup(
    name="num2wordshindi",
    version="0.0.1",
    author="Parmod Sihag",
    author_email="parmodsihag028@gmail.com",
    description="A packeg to convert number to string iin hindi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Parmodsihag/num2wordshindi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
