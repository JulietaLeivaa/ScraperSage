"""
Setup configuration for MyScrapeLib - A comprehensive web scraping and content summarization library.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A comprehensive web scraping and content summarization library"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="ScraperSage",
    version="1.0.0",
    author="Akil",
    author_email="akilaskarali@gmail.com",  # Replace with your actual email
    description="A comprehensive web scraping and content summarization library with AI-powered features",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/akillabs/ScraperSage",  # Replace with your actual repo URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    keywords="web scraping, content summarization, search, AI, playwright, gemini",
    project_urls={
        "Bug Reports": "https://github.com/akillabs/ScraperSage/issues",
        "Source": "https://github.com/akillabs/ScraperSage",
        "Documentation": "https://github.com/akillabs/ScraperSage/blob/main/README.md",
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "ScraperSage=ScraperSage.cli:main",  # Optional CLI entry point
        ],
    },
    include_package_data=True,
    zip_safe=False,
)