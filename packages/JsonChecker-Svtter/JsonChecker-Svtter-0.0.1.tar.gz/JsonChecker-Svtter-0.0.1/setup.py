import setuptools

with open("README.md", "r") as f:
    long_description = f.read()



setuptools.setup(
    name="JsonChecker-Svtter", # Replace with your own username
    version="0.0.1",
    author="Svtter",
    author_email="svtter@qq.com",
    description="Check the python dict type via json file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Svtter/JsonChecker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
