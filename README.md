# Code-to-Docs Agent Demo

A minimal demonstration of automated documentation generation from Python code using docstrings and GitHub Actions.

## 🎯 Overview

This repository showcases an automated workflow that:

- 📝 **Parses Python docstrings** from source code
- 📚 **Generates Markdown documentation** automatically
- 🔄 **Updates docs via GitHub Actions** on every code change
- 🌐 **Serves docs with MkDocs** for beautiful presentation

## 🚀 Quick Start

### 1. Generate Documentation Locally

```bash
# Clone the repository
git clone https://github.com/marinatenhave/code-to-docs-agent-demo.git
cd code-to-docs-agent-demo

# Install dependencies
pip install -r requirements.txt

# Generate API documentation
python agent/doc_generator.py

# Serve the docs locally
mkdocs serve
```

### 2. Automatic Updates

Documentation is automatically updated when:
- Code changes are pushed to the `main` branch
- Pull requests modify files in the `src/` directory

The GitHub Action will:
1. Parse docstrings from Python files
2. Generate updated Markdown in `docs/api/`
3. Commit changes back to the repository
4. Comment on PRs with update status

## 📁 Project Structure

```
code-to-docs-agent-demo/
├── src/                          # Python source code
│   ├── __init__.py              # Package initialization
│   ├── calculator.py            # Calculator functions and classes
│   └── utils.py                 # Utility functions
├── docs/                        # Documentation
│   ├── index.md                # Main documentation page
│   └── api/                    # Auto-generated API documentation
│       ├── index.md            # API reference index
│       ├── calculator.md       # Calculator module docs
│       └── utils.md            # Utils module docs
├── agent/                       # Documentation generation
│   └── doc_generator.py        # Docstring parser and markdown generator
├── .github/workflows/           # GitHub Actions
│   └── update-docs.yml         # Auto-documentation workflow
├── mkdocs.yml                  # MkDocs configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ How It Works

### 1. Source Code with Docstrings

Python modules in `src/` contain well-documented functions and classes:

```python
def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a (float): The first number
        b (float): The second number
        
    Returns:
        float: The sum of a and b
    """
    return a + b
```

### 2. Documentation Agent

The `agent/doc_generator.py` script:
- Uses Python's `ast` module to parse source code
- Extracts docstrings from functions and classes
- Converts docstrings to formatted Markdown
- Generates API documentation in `docs/api/`

### 3. GitHub Actions Integration

The workflow in `.github/workflows/update-docs.yml`:
- Triggers on code changes in `src/`
- Runs the documentation generator
- Commits updated documentation
- Comments on PRs with status updates

### 4. MkDocs Integration

The `mkdocs.yml` configuration:
- Uses Material theme for beautiful docs
- Includes syntax highlighting
- Organizes documentation with navigation

## 🔧 Customization

### Adding New Modules

1. Add Python files to `src/` with proper docstrings
2. Run `python agent/doc_generator.py` to generate docs
3. Documentation will appear in `docs/api/`

### Modifying Documentation Style

Edit `agent/doc_generator.py` to customize:
- Markdown formatting
- Section organization
- Docstring parsing rules

### Changing MkDocs Theme

Modify `mkdocs.yml` to:
- Change themes and colors
- Add plugins and extensions
- Customize navigation structure

## 📖 Examples

See the generated documentation:
- [Calculator Module](docs/api/calculator.md) - Basic arithmetic operations
- [Utils Module](docs/api/utils.md) - Helper functions

## 🤝 Contributing

1. Fork the repository
2. Make changes to code in `src/`
3. Create a pull request
4. Documentation will be automatically updated!

## 📄 License

This project is released into the public domain. Feel free to use it as a template for your own projects.

---

**Made with ❤️ to demonstrate automated documentation workflows**
