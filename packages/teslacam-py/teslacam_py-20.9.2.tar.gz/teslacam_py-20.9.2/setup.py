from os import path
from setuptools import setup, find_packages

here = path.dirname(__file__)

with open(path.join(here, "teslacam/VERSION"), encoding="utf-8") as file:
    version = file.read()

setup(
    name="teslacam_py",
    version=version,
    description="TeslaCam uploader",
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[
        "pyyaml>=5.3",
        "azure-storage-blob>=12.1.0",
        "sh>=1.12.14",
        "flask>=1.1.1",
        "chump>=1.6.0"
    ],
    entry_points={"console_scripts": ["teslacam = teslacam.__main__:main"]}
)