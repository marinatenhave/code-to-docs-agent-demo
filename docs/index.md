# Code-to-Docs Agent Demo

Welcome to the **Code-to-Docs Agent Demo**! This project demonstrates how to automatically generate and update documentation from Python code docstrings.

## Overview

This repository showcases an automated workflow that:

1. **Parses Python docstrings** from source code
2. **Generates Markdown documentation** in the `docs/api/` directory
3. **Automatically updates docs** when code changes via GitHub Actions

## Features

- 🐍 **Simple Python modules** with well-documented functions and classes
- 📚 **Automatic API documentation** generation from docstrings
- 🔄 **GitHub Actions integration** for continuous documentation updates
- 📖 **MkDocs-ready structure** for beautiful documentation sites

## Getting Started

### Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the documentation agent: `python agent/doc_generator.py`
4. Serve the docs locally: `mkdocs serve`

### API Reference

The API documentation is automatically generated from the source code docstrings. Check out the [API Reference](api/index.md) section to explore the available modules and functions.

## Project Structure

```
code-to-docs-agent-demo/
├── src/                    # Python source code
│   ├── __init__.py
│   ├── calculator.py      # Main calculator module
│   └── utils.py           # Utility functions
├── docs/                  # Documentation
│   ├── index.md          # This file
│   └── api/              # Auto-generated API docs
├── agent/                # Documentation generation
│   └── doc_generator.py  # Docstring parser and doc generator
├── .github/workflows/    # GitHub Actions
│   └── update-docs.yml   # Auto-update workflow
└── mkdocs.yml           # MkDocs configuration
```