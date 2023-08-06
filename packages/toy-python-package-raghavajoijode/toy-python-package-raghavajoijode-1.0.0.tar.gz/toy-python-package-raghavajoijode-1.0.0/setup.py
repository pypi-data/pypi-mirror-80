
from example_pkg.utils import package_name, package_version
import setuptools


def readme():
    with open('README.md', 'r') as f:
        read_me = f.read()
    return read_me

with open('requirements.txt', 'r') as f:
    required_dependencies = f.read().splitlines()


setuptools.setup(
    name=package_name, # Replace with your own username
    version=package_version,
    author="Raghava Joijode",
    author_email="raghava.joijode@gmail.com",
    description="A toy python package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/raghavajoijode/toy-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=required_dependencies
)