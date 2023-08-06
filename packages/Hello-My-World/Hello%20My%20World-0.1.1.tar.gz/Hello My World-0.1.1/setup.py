import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
    "Homepage": "https://github.com/eocode/hello_my_world",
    "Issue tracker": "https://github.com/eocode/hello_my_world/issues",
    "Code": "https://github.com/eocode/hello_my_world",
    "Documentation": "https://github.com/eocode/hello_my_world/wiki",
}

setuptools.setup(
    name='Hello My World',
    version='0.1.1',
    author='eocode',
    author_email='hola@eliasojedamedina.com',
    description='A simple package for python',
    long_description_content_type="text/markdown",
    long_description=open("README.md").read()
    + "\n\n"
    + open("CHANGELOG.md").read()
    + open("AUTHORS.md").read(),
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls=project_urls,
    install_requires=[],
    python_requires=">=3.6",
)
