from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="utiltools",
    version="1.0.0",
    author="UtilTools Contributors",
    description="A comprehensive utility toolkit for automation and productivity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gencersarp/UtilTools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "requests>=2.26.0",
        "psutil>=5.8.0",
        "pyyaml>=5.4.1",
        "watchdog>=2.1.0",
        "schedule>=1.1.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "utiltools=utiltools.cli:main",
        ],
    },
)
