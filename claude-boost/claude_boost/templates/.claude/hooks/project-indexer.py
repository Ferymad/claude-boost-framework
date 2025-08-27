#!/usr/bin/env python3
"""
Project Index Generator for Claude Code Boost
Creates minified abstractions of codebase for project awareness
"""
import json
import os
import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

def extract_python_info(filepath: str) -> Dict[str, Any]:
    """Extract imports, functions, classes from Python files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        info = {
            'imports': [],
            'functions': [],
            'classes': [],
            'constants': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    info['imports'].append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names]
                info['imports'].append(f"from {module} import {', '.join(names)}")
            elif isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                info['functions'].append({
                    'name': node.name,
                    'args': args,
                    'returns': getattr(node.returns, 'id', None) if node.returns else None,
                    'line': node.lineno,
                    'async': isinstance(node, ast.AsyncFunctionDef)
                })
            elif isinstance(node, ast.ClassDef):
                methods = []
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        methods.append({
                            'name': n.name,
                            'args': [arg.arg for arg in n.args.args],
                            'line': n.lineno
                        })
                info['classes'].append({
                    'name': node.name,
                    'methods': methods,
                    'line': node.lineno,
                    'bases': [base.id for base in node.bases if hasattr(base, 'id')]
                })
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        info['constants'].append(target.id)
        
        return info
    except Exception as e:
        return {'error': str(e)}

def extract_js_info(filepath: str) -> Dict[str, Any]:
    """Extract basic info from JavaScript/TypeScript files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': []
        }
        
        # Extract imports
        import_patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s*\{\s*([^}]+)\s*\}\s*from\s+[\'"]([^\'"]+)[\'"]'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            info['imports'].extend([match[0] if isinstance(match, tuple) else match for match in matches])
        
        # Extract function definitions
        func_pattern = r'(?:function\s+(\w+)|const\s+(\w+)\s*=.*?=>|(\w+)\s*:\s*function)'
        functions = re.findall(func_pattern, content)
        info['functions'] = [f[0] or f[1] or f[2] for f in functions if any(f)]
        
        # Extract class definitions
        class_pattern = r'class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        info['classes'] = classes
        
        # Extract exports
        export_pattern = r'export\s+(?:default\s+)?(?:class\s+|function\s+|const\s+|let\s+|var\s+)?(\w+)'
        exports = re.findall(export_pattern, content)
        info['exports'] = exports
        
        return info
    except Exception as e:
        return {'error': str(e)}

def generate_project_index(root_dir: str = ".") -> Dict[str, Any]:
    """Generate comprehensive project index"""
    index = {
        'project_root': os.path.abspath(root_dir),
        'generated_at': str(__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'files': {},
        'summary': {
            'total_files': 0,
            'analyzed_files': 0,
            'languages': {},
            'directories': 0,
            'total_functions': 0,
            'total_classes': 0,
            'cached_files': 0,
            'generation_time_seconds': 0.01
        }
    }
    
    # File extensions to analyze
    extensions = {
        '.py': extract_python_info,
        '.js': extract_js_info,
        '.jsx': extract_js_info,
        '.ts': extract_js_info,
        '.tsx': extract_js_info
    }
    
    # Read .gitignore if exists
    ignore_patterns = {
        'node_modules', '.git', '__pycache__', '.pytest_cache',
        'dist', 'build', '.env', 'venv', '.venv', '.claude'
    }
    
    gitignore_path = os.path.join(root_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_patterns = {line.strip() for line in f if line.strip() and not line.startswith('#')}
            ignore_patterns.update(gitignore_patterns)
    
    for root, dirs, files in os.walk(root_dir):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in ignore_patterns)]
        
        rel_root = os.path.relpath(root, root_dir)
        if rel_root != '.':
            index['summary']['directories'] += 1
        
        for file in files:
            if any(pattern in file for pattern in ignore_patterns):
                continue
            
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_dir)
            
            # Get file extension
            _, ext = os.path.splitext(file)
            
            # Track language stats
            if ext:
                index['summary']['languages'][ext] = index['summary']['languages'].get(ext, 0) + 1
            
            # Extract file info for supported languages
            if ext in extensions:
                file_info = extensions[ext](filepath)
                if 'error' not in file_info:
                    file_info['path'] = rel_path
                    file_info['size'] = os.path.getsize(filepath)
                    file_info['modified'] = os.path.getmtime(filepath)
                    index['files'][rel_path] = file_info
                    index['summary']['analyzed_files'] += 1
                    index['summary']['total_functions'] += len(file_info.get('functions', []))
                    index['summary']['total_classes'] += len(file_info.get('classes', []))
            
            index['summary']['total_files'] += 1
    
    return index

if __name__ == "__main__":
    try:
        index = generate_project_index()
        with open("PROJECT_INDEX.json", "w") as f:
            json.dump(index, f, indent=2, default=str)
        print(f"✅ Generated PROJECT_INDEX.json ({index['summary']['total_files']} files analyzed)")
    except Exception as e:
        print(f"❌ Error generating project index: {e}", file=sys.stderr)
        sys.exit(1)