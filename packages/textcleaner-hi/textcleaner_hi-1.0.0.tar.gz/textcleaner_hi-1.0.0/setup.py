from setuptools import setup

def readMe():
    with open("README.md","r") as f:
        README = f.read()
    return README

setup(
    name = "textcleaner_hi",
    version = "1.0.0",
    description = "A Python package to extract hindi characters.",
    long_description = readMe(),
    long_description_content_type = "text/markdown",
    author = "Chhavi Trivedi, Naman Jain, Ms. Gayatri Venugopal",
    author_email = "chhavi7320@gmail.com, n.jnamanjain2001@gmail.com, gayatrivenugopal3@gmail.com",
    license = "MIT License",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages = ["hindiExtract"],
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "extract=hindiExtract.clean:main",
        ]
    },
)