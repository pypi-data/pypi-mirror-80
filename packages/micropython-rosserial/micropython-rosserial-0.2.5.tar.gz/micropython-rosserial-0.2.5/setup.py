import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micropython-rosserial", # Replace with your own username
    version="0.2.5",
    author="Steven Silva Mendoza",
    author_email="sasilva1998@gmail.com",
    description="A package done in order to use rosserial with micropython.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FunPythonEC/uPy-rosserial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
