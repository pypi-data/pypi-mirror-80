import os, re, setuptools

varsVals = {}

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = ""

if os.path.isfile("variables"):
    try:
        with open("variables", "r") as fh:
            variables = fh.read().strip().split("\n")
        for v in variables:
            key, value = v.split("=")
            varsVals[key] = re.sub("['\"]", "", value)
    except:
        pass

setuptools.setup(
    name=varsVals["NAME"],
    version=varsVals["VERSION"],
    author=varsVals["AUTHOR"],
    author_email=varsVals["AUTHOR_EMAIL"],
    description=varsVals["DESCRIPTION"],
    install_requires=['telegram','configparser'],
    url=varsVals["URL"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)