from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-boost",
    version="1.0.0",
    author="Claude Code Boost Team",
    author_email="hello@claude-boost.dev",
    description="Supercharge Claude Code with one command - Get 37% productivity boost, <5% code duplication, and never lose context again",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/claude-boost",
    project_urls={
        "Bug Reports": "https://github.com/username/claude-boost/issues",
        "Source": "https://github.com/username/claude-boost",
        "Documentation": "https://claude-boost.dev/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - keep it lightweight
    ],
    entry_points={
        "console_scripts": [
            "claude-boost=claude_boost.cli:main",
        ],
    },
    package_data={
        "claude_boost": [
            "templates/.claude/*",
            "templates/.claude/**/*",
        ]
    },
    include_package_data=True,
    keywords=[
        "claude", "claude-code", "ai", "development", "productivity", 
        "automation", "code-generation", "ai-assistant", "developer-tools"
    ],
)