#!/usr/bin/env python3
"""
Documentation Generator Agent

This script automatically parses Python docstrings from the src/ directory
and generates Markdown documentation in the docs/api/ directory.
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class DocstringParser:
    """Parser for extracting and formatting docstrings from Python modules."""
    
    def __init__(self, src_dir: str = "src", docs_dir: str = "docs/api"):
        self.src_dir = Path(src_dir)
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_module(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a Python module and extract docstrings.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing module information and docstrings
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return {}
        
        module_info = {
            'name': file_path.stem,
            'docstring': ast.get_docstring(tree),
            'functions': [],
            'classes': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Skip private functions
                    func_info = self._parse_function(node)
                    if func_info:
                        module_info['functions'].append(func_info)
            
            elif isinstance(node, ast.ClassDef):
                class_info = self._parse_class(node)
                if class_info:
                    module_info['classes'].append(class_info)
        
        return module_info
    
    def _parse_function(self, node: ast.FunctionDef) -> Optional[Dict[str, Any]]:
        """Parse a function node and extract its information."""
        docstring = ast.get_docstring(node)
        if not docstring:
            return None
        
        # Extract function signature
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if hasattr(arg, 'annotation') and arg.annotation:
                if hasattr(arg.annotation, 'id'):
                    arg_str += f": {arg.annotation.id}"
                elif hasattr(arg.annotation, 'attr'):
                    arg_str += f": {arg.annotation.attr}"
            args.append(arg_str)
        
        # Handle return annotation
        return_type = ""
        if node.returns:
            if hasattr(node.returns, 'id'):
                return_type = node.returns.id
            elif hasattr(node.returns, 'attr'):
                return_type = node.returns.attr
        
        return {
            'name': node.name,
            'docstring': docstring,
            'args': args,
            'return_type': return_type
        }
    
    def _parse_class(self, node: ast.ClassDef) -> Optional[Dict[str, Any]]:
        """Parse a class node and extract its information."""
        docstring = ast.get_docstring(node)
        if not docstring:
            return None
        
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                method_info = self._parse_function(item)
                if method_info:
                    methods.append(method_info)
        
        return {
            'name': node.name,
            'docstring': docstring,
            'methods': methods
        }
    
    def _format_docstring_section(self, docstring: str) -> str:
        """Format a docstring into markdown, handling Args, Returns, etc."""
        if not docstring:
            return ""
        
        lines = docstring.strip().split('\n')
        formatted_lines = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Check for section headers
            if line.lower().startswith(('args:', 'arguments:', 'parameters:')):
                current_section = 'args'
                formatted_lines.append("\n**Arguments:**\n")
                continue
            elif line.lower().startswith(('returns:', 'return:')):
                current_section = 'returns'
                formatted_lines.append("\n**Returns:**\n")
                continue
            elif line.lower().startswith(('raises:', 'raise:')):
                current_section = 'raises'
                formatted_lines.append("\n**Raises:**\n")
                continue
            elif line.lower().startswith(('example:', 'examples:')):
                current_section = 'example'
                formatted_lines.append("\n**Example:**\n")
                continue
            elif line.lower().endswith(':') and len(line.split()) == 1:
                current_section = 'other'
                formatted_lines.append(f"\n**{line}**\n")
                continue
            
            # Format content based on current section
            if current_section == 'args' and line and ':' in line:
                # Format argument descriptions
                formatted_lines.append(f"- `{line}`")
            elif current_section == 'example' and line.startswith('>>>'):
                # Format code examples
                formatted_lines.append(f"```python\n{line}\n```")
            elif line:
                formatted_lines.append(line)
            else:
                formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def generate_module_docs(self, module_info: Dict[str, Any]) -> str:
        """Generate markdown documentation for a module."""
        if not module_info:
            return ""
        
        doc_lines = []
        
        # Module title and description
        doc_lines.append(f"# {module_info['name']}.py\n")
        
        if module_info.get('docstring'):
            doc_lines.append(self._format_docstring_section(module_info['docstring']))
            doc_lines.append("\n---\n")
        
        # Functions section
        if module_info.get('functions'):
            doc_lines.append("## Functions\n")
            
            for func in module_info['functions']:
                doc_lines.append(f"### {func['name']}")
                
                # Function signature
                args_str = ', '.join(func['args'])
                return_str = f" -> {func['return_type']}" if func['return_type'] else ""
                doc_lines.append(f"```python\n{func['name']}({args_str}){return_str}\n```\n")
                
                # Function docstring
                if func['docstring']:
                    doc_lines.append(self._format_docstring_section(func['docstring']))
                doc_lines.append("\n---\n")
        
        # Classes section
        if module_info.get('classes'):
            doc_lines.append("## Classes\n")
            
            for cls in module_info['classes']:
                doc_lines.append(f"### {cls['name']}\n")
                
                if cls['docstring']:
                    doc_lines.append(self._format_docstring_section(cls['docstring']))
                    doc_lines.append("\n")
                
                # Class methods
                if cls.get('methods'):
                    doc_lines.append("#### Methods\n")
                    for method in cls['methods']:
                        doc_lines.append(f"##### {method['name']}")
                        
                        args_str = ', '.join(method['args'])
                        return_str = f" -> {method['return_type']}" if method['return_type'] else ""
                        doc_lines.append(f"```python\n{method['name']}({args_str}){return_str}\n```\n")
                        
                        if method['docstring']:
                            doc_lines.append(self._format_docstring_section(method['docstring']))
                        doc_lines.append("\n")
                
                doc_lines.append("---\n")
        
        return '\n'.join(doc_lines)
    
    def generate_all_docs(self):
        """Generate documentation for all Python modules in the src directory."""
        print(f"Generating documentation from {self.src_dir} to {self.docs_dir}")
        
        # Find all Python files
        python_files = list(self.src_dir.glob("*.py"))
        
        if not python_files:
            print(f"No Python files found in {self.src_dir}")
            return
        
        # Generate API index
        api_index_lines = ["# API Reference\n"]
        api_index_lines.append("This section contains automatically generated documentation from the source code.\n")
        
        for py_file in python_files:
            if py_file.name == '__init__.py':
                continue
            
            print(f"Processing {py_file.name}...")
            
            # Parse the module
            module_info = self.parse_module(py_file)
            
            if not module_info:
                continue
            
            # Generate markdown documentation
            markdown_content = self.generate_module_docs(module_info)
            
            # Write to docs/api/
            output_file = self.docs_dir / f"{py_file.stem}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Generated documentation: {output_file}")
            
            # Add to API index
            api_index_lines.append(f"- [{module_info['name']}]({py_file.stem}.md)")
        
        # Write API index
        api_index_file = self.docs_dir / "index.md"
        with open(api_index_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(api_index_lines))
        
        print(f"Generated API index: {api_index_file}")
        print("Documentation generation complete!")


def main():
    """Main entry point for the documentation generator."""
    # Change to the repository root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    # Generate documentation
    parser = DocstringParser()
    parser.generate_all_docs()


if __name__ == "__main__":
    main()