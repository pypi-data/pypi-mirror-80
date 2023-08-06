from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="oaas_grpc",
    version="1.0.2",
    description="oaas_grpc",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    install_requires=[
        "grpc-stubs==1.24.2",
        "oaas",
        "oaas_registry_api",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "oaas_grpc": ["py.typed"],
    },
)
