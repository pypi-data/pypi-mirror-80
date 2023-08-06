import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
    "Homepage": "https://github.com/eocode/First-Python-Package",
    "Issue tracker": "https://github.com/eocode/First-Python-Package/issues",
    "Code": "https://github.com/eocode/First-Python-Package",
    "Documentation": "https://github.com/eocode/First-Python-Package/wiki",
}

setuptools.setup(
    name="say_message",
    version="0.0.4",
    author="Elias Ojeda Medina",
    author_email="hola@eliasojedamedina.com",
    description="A library that print a message.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="https://github.com/eocode/First-Python-Package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls=project_urls,
    python_requires=">=3.6",
)