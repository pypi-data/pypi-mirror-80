import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htmlcomparator", # Replace with your own username
    version="0.1.0",
    author="Mengjia Zhao",
    author_email="lucyzmj0914@gmail.com",
    description="An html comparator that can output the differences between html code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/in-the-ocean/htmlcomparator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)