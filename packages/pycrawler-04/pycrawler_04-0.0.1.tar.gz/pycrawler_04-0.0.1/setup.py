import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycrawler_04", # Replace with your own username
    version="0.0.1",
    author="palak_agrawal",
    author_email="palakagrawaljk@gmail.com",
    description="A crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.corp.adobe.com/yanand/PY_4",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
	
