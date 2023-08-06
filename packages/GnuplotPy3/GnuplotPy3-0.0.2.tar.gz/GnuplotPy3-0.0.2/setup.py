import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GnuplotPy3",
    version="0.0.2",
    author="Cong Wang",
    author_email="wangimagine@gmail.com",
    description="A minimal Python wrapper for Gnuplot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carbonscott/GnuplotPy3",
    keywords = ['Gnuplot', 'wrapper'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
