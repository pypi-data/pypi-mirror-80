import io

import setuptools

with io.open('./README.rst', encoding='utf-8') as f:
    readme = f.read()

setuptools.setup(
    name="pip_helloworld",
    version="0.0.12",
    author="evoup",
    author_email="evoex123@gmail.com",
    description="A small example package",
    long_description=readme,
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
