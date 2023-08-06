import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gamayun-utils",
    version="0.2.0",
    author="Ivan Brko",
    author_email="ivan.brko@outlook.com",
    description="Python utils for writing gamayun job scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivan-brko/GamayunPyUtils",
    packages=setuptools.find_packages(),
    install_requires=[
          'grpcio==1.30.0',
          'protobuf==3.13.0'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
