import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vpcolab", # Replace with your own username
    version="0.1.3",
    author="jcoady",
    author_email="jcoady@shaw.ca",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jcoady/vpcolab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'vpcolab': ['vpython_data/*',
                              'vpython_libraries/*',
                              'vpython_libraries/images/*']},
    python_requires='>=3.6',
)