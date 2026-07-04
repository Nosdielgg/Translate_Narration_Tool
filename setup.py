"""
Setup configuration for Translate & Narration Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="translate-narrate-tool",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python desktop application for translation and text-to-speech narration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/translate-narrate-tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "edge-tts>=6.1.0",
        "deep-translator>=1.11.4",
        "python-docx>=0.8.11",
    ],
    entry_points={
        "console_scripts": [
            "translate-narrate=src.main:main",
        ],
    },
)
