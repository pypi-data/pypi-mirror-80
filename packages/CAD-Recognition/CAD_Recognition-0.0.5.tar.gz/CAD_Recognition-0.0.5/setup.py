import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CAD_Recognition",
    version="0.0.5",
    author="francis",
    author_email="francirk@163.com",
    description="CAD Recognition.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/imgkernel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['tensorflow','Keras','kmeans-smote','python-speech-features'],
    python_requires='==3.5',
)
