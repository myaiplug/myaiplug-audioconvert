from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="myaiplug-audioconvert",
    version="0.1.0",
    author="MyAIPlug",
    description="High quality audio converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myaiplug/myaiplug-audioconvert",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydub>=0.25.1",
        "ffmpeg-python>=0.2.0",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "audioconvert=audioconvert.cli:main",
        ],
    },
)
