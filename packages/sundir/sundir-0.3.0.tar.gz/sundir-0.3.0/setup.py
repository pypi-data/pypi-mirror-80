import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.read().splitlines()


setuptools.setup(
    name="sundir",  # Replace with your own username
    version="0.3.0",
    description="Sun Direction Calculator.",
    author="Takayuki Matsuda",
    author_email="taka.matsuda@simgics.co.jp",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/simgics/sundir",
    packages=setuptools.find_packages(),
    install_requires=install_requirements,
    entry_points={"console_scripts": ["sundir=sundir.sun_dir_calc:main",]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
