import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tablear", # Replace with your own username
    version="1.0.1",
    author="Julie Ganeshan",
    author_email="HeavenlyQueen@outlook.com",
    description="Print a UI and detect it with camera",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sanjay-Ganeshan/TableAR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.7',
    install_requires=[
        "opencv-python>=4.2.0.34",
        "numpy>=1.18.4",
    ],
    include_package_data=True
)