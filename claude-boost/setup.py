from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-boost",
    version="0.9.0-beta",
    author="Claude Code Boost Team",
    author_email="hello@claude-boost.dev",
    description="[BETA] Claude Code Performance Enhancement System - Advanced framework for AI development with project awareness, blind validation, and workflow automation. Beta testing in progress.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ferymad/claude-boost-framework",
    project_urls={
        "Bug Reports": "https://github.com/Ferymad/claude-boost-framework/issues",
        "Source": "https://github.com/Ferymad/claude-boost-framework",
        "Documentation": "https://github.com/Ferymad/claude-boost-framework#readme",
        "Homepage": "https://github.com/Ferymad/claude-boost-framework",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
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