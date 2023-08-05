from setuptools import setup

setup(
    name="gspackage", # Replace with your own username
    version="4.1.2",
    author="Swapnali Kapare",
    author_email="swapnalikapare02@gmail.com",
    description="A small example package",
    long_description="This is very usefull package...",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['gspackage'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)