from distutils.core import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read().strip()
with open(path.join(this_directory, "LICENSE"), encoding="utf-8") as f:
    license = f.read()


setup(
    name="TextBase",
    version="0.14",
    description="TextBase library to manipulate DBText style data files",
    description_content_type="text/plain",
    long_description=long_description,
    long_description_content_type="text/rst",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Etienne Posthumus",
    author_email="posthumus@brill.com",
    url="https://gitlab.com/brillpublishers/code/textbase",
    py_modules=["textbase"],
)
