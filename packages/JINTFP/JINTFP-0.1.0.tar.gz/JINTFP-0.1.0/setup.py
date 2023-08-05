import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JINTFP",
    version="0.1.0",
    author="grasshopperTrainer",
    author_email="grasshoppertrainer@gmail.com",
    description="Python package for creating node-based function pipeline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grasshopperTrainer/JINTFP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords='function pipeline, functional pipeline, pipeline',
    python_requires='>=3'
)
