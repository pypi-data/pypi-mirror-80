import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="analyseGoogleMyActivity",
    version="0.1",
    description="Generates Report of Sleep-Time, Sleep-Routine and App-Usage using Data from Google MyActivity : myactivity.google.com",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/superuser789/analyseGoogleMyActivity/",
    author="Nitin Singh",
    author_email="acc4nitin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["analyseGoogleMyActivity"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "matplotlib"],
)