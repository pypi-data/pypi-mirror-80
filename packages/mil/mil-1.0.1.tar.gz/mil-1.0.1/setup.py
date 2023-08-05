import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mil", 
    version="1.0.1",
    author="Rosas, Alberto",
    author_email="alberto.rosas@upc.edu",
    description="Multiple instance learning package for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rosasalberto/mil",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)