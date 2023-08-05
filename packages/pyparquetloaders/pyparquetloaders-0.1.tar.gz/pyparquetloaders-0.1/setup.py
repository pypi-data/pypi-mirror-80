import setuptools

with open("README.md") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="pyparquetloaders",
    version="0.1",
    author="Kamron Bhavnagri",
    author_email="kamwithk@tuta.io",
    description="Easy, efficient and Pythonic data loading of Parquet files for PyTorch-based libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KamWithK/PyParquetLoaders",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    install_requires=["pyarrow", "torch"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    extras_require={"petastorm": "petastorm", "transformers": "transformers[torch]", "allennlp": "allennlp"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Utilities"
    ],
    python_requires=">=3.6"
)