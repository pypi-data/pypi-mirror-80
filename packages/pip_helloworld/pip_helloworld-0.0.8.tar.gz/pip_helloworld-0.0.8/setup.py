import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except Exception as e:
    long_description = "long description"

setuptools.setup(
    name="pip_helloworld", # Replace with your own username
    version="0.0.8",
    author="evoup",
    author_email="evoex123@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
