import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="questionare", # Replace with your own username
    version="",
    author="CraftYun83",
    author_email="craftyun83@gmail.com",
    description="Easiest way to make a simple survey!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CraftYun83/Questionare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)