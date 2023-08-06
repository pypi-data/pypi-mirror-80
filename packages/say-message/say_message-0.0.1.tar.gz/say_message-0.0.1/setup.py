import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="say_message", 
    version="0.0.1",
    author="Elias Ojeda Medina",
    author_email="hola@eliasojedamedina.com",
    description="A library that print a message.",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url="https://github.com/eocode/First-Python-Package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)