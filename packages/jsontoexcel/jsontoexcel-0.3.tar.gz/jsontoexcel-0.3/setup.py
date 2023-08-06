import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsontoexcel", # Replace with your own username
    version="0.03",
    author="Akriti Anand",
    description="Package to convert complex json objects into excel",
    long_description_content_type="text/markdown",
    url="https://github.com/akritianand/JsonToExcel",
    packages=['jsontoexcel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
