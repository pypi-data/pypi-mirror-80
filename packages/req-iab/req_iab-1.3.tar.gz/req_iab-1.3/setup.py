import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="req_iab",
    description="I_am_back的requests项目",
    author="I_am_back",
    author_email="2682786816@qq.com",
    version="1.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Development Status :: 6 - Mature",
    ],
    packages=setuptools.find_packages(),
)
