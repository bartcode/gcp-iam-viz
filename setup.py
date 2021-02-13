"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_namespace_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./src/iamviz/__init__.py") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

setup(
    name="iamviz",
    author="Bart Hazen",
    author_email="hazenbart@gmail.com",
    description="Visualise IAM policies within GCP.",
    version=VERSION.get("__version__", "0.0.0"),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", exclude=["tests"]),
    include_package_data=True,
    package_data={"iamviz": ["src/iamviz/package_data/*"]},
    install_requires=[
        "setuptools>=45.0",
        "google-cloud-asset~=2.2",
        "google-cloud-storage~=1.36",
        "neomodel~=4.0",
        "pyyaml~=5.4",
    ],
    entry_points={
        "console_scripts": [
            "iamviz=iamviz.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
    ],
)
