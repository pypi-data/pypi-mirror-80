import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="siarnaq",
        version="1.0.1",
        author="Thierry P.G. DECKER",
        author_email="mail@thierry-decker.com",
        description="A conversion library",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/thierrydecker/siarnaq",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.8',
)
