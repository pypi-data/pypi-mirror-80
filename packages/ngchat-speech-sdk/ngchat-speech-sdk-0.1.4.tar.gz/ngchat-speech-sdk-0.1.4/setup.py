import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ngchat-speech-sdk",
    version="0.1.4",
    author="Seasalt.ai",
    author_email="info@seasalt.ai",
    description="ngChat Speech SDK: Realize ngChat Speech-to-Text recognition and Text-to-Speech synthesis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
