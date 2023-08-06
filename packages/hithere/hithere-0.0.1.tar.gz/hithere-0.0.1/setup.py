from setuptools import setup

with open("README.md","r") as fh:
    long_description=fh.read()
setup(
    name='hithere',
    version='0.0.1',
    description="Say hi !!",
    py_modules=["hithere"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "blessings ~= 1.7",

    ],
    extras_require={
        "dev":[
            "pytest>=3.7.4",

        ],
    },
    url="https://github.com/abinashstack/pypi",
    author="Abinash Gogoi",
    author_email="abinash.gogoi55@gmail.com"


)