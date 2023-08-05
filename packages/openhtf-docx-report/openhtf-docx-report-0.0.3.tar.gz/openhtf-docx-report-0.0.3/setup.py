import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openhtf-docx-report", 
    version="0.0.3",
    author="Kevin Pulley",
    author_email="kpulley@imaginecommunications.com",
    description="Simple Openhtf MS-Word document test report callback",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UndyingScroll",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       "docx",
       "docxtpl",
       "matplot",
       "python-docx"
   ],
    python_requires='>=3.6',
)
