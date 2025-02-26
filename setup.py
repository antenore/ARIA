"""Setup script for ARIA."""
from pathlib import Path
from setuptools import setup, find_packages

# Read README.md if it exists
readme_path = Path("README.md")
long_description = readme_path.read_text() if readme_path.exists() else ""

setup(
    name="aria-framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0.1",
        "click>=8.1.7",
        "rich>=13.7.0",
        "pydantic>=2.6.1",
        "jsonschema>=4.21.1"
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'flake8',
            'mypy',
            'types-PyYAML',
        ],
        'docs': [
            'mkdocs',
            'mkdocs-material',
            'mkdocs-minify-plugin',
        ],
    },
    entry_points={
        'console_scripts': [
            'ariacli=aria.cli:cli',
        ],
    },
    author="Antenore Gatta",
    author_email="antenore@simbiosi.org",
    description="AI Participation Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antenore/ARIA",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
