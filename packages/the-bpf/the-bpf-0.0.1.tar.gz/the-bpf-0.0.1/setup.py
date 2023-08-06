import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="the-bpf", 
    version="0.0.1",
    scripts=['the-bpf'] ,
    author="Gokul Krishnan",
    author_email="cipherweb777@gmail.com",
    description="for automation and security audidting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FraternityInfoSec/Blackpearl-framework.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
