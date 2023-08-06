import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wavimedical", 
    version="0.0.2",
    author="Clayton Schneider",
    author_email="clayton.schneider@colorado.edu",
    description="WAVi Medical's EEG Analysis and ML Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canlab/WAViMedEEG",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.2',
)
