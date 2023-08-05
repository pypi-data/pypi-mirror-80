import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyclilib",
    version="0.2.0",
    author="Mark Diez",
    author_email="markediez@gmail.com",
    description="Build CLI Tools with ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markediez/clilib",
    packages=setuptools.find_packages('src'),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pylogrus'
    ]
)
