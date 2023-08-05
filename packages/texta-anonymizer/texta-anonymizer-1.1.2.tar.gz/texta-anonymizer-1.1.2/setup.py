import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_requirements(fname):
    req_string = read(fname)
    return [req.strip() for req in req_string.split("\n") if not req.strip().startswith("http")]

def get_dependency_links(fname):
    req_string = read(fname)
    return [req.strip() for req in req_string.split("\n") if req.strip().startswith("http")]

setup(
    name = "texta-anonymizer",
    version = read("VERSION"),
    author = "TEXTA",
    author_email = "info@texta.ee",
    description = ("texta-anonymizer"),
    license = "GPLv3",
    packages = [
        "texta_anonymizer",
        "texta_anonymizer.extractors"
    ],
    data_files = ["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description = read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.texta.ee/texta/texta-anonymizer-python",
    install_requires = get_requirements("requirements.txt"),
    dependency_links = get_dependency_links("requirements.txt"),
    include_package_data = True
)
