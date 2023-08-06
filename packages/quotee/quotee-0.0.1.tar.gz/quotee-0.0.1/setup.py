import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="quotee",
    version="0.0.1",
    author="Mahmoud Ibrahiam",
    author_email="golldenhouse@gmail.com",
    description="Small App To get Quotes depend on Zenquotes api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/officialzoka/Quotee.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)