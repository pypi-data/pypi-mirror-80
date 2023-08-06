import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdf2txt-pkg-jeff", 
    version="1.0.0",
    author="Jeff Merino-Ott",
    author_email="jeff@coffeecoder.com",
    description="Converts a PDF to Text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jcott28/pdf2txt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
