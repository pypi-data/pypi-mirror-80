import setuptools

with open("README.md", "rb") as fh:
    print(fh.read())
    long_description = fh.read()

setuptools.setup(
    name="chiyi",
    version="0.0.3",
    author="chiyi",
    author_email="chishishuan@gmail.com",
    description="Image chiyi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/chiyi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
