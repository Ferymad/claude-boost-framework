#!/usr/bin/env python3
"""
Project Index Generator for Claude Code
Creates minified abstractions of codebase for project awareness
Prevents code duplication by providing comprehensive project structure overview
"""
import json
import os
import ast
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Any

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
            'constants': [],
            'exports': []
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
                returns = ast.unparse(node.returns) if node.returns else None
                info['functions'].append({
                    'name': node.name,
                    'args': args,
                    'returns': returns,
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
                    'bases': [ast.unparse(base) for base in node.bases]
                })
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        info['constants'].append(target.id)
        
        return info
    except Exception as e:
        return {'error': str(e), 'filepath': filepath}

def extract_js_info(filepath: str) -> Dict[str, Any]:
    """Extract basic info from JavaScript/TypeScript files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': [],
            'interfaces': [],
            'types': []
        }
        
        # Extract imports (ES6 modules)
        import_patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s*\{\s*([^}]+)\s*\}\s*from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            info['imports'].extend(matches)
        
        # Extract function definitions
        func_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{',
            r'(\w+)\s*:\s*(?:async\s+)?function\s*\([^)]*\)',
            r'async\s+function\s+(\w+)\s*\([^)]*\)'
        ]
        for pattern in func_patterns:
            functions = re.findall(pattern, content)
            info['functions'].extend(functions)
        
        # Extract class definitions
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        classes = re.findall(class_pattern, content)
        for class_match in classes:
            class_name = class_match[0]
            extends = class_match[1] if class_match[1] else None
            # Find methods in this class (simplified)
            class_methods = re.findall(rf'(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{{', content)
            info['classes'].append({
                'name': class_name,
                'extends': extends,
                'methods': class_methods[:10]  # Limit to first 10 methods
            })
        
        # Extract TypeScript interfaces
        interface_pattern = r'interface\s+(\w+)(?:\s+extends\s+[\w,\s]+)?\s*\{'
        interfaces = re.findall(interface_pattern, content)
        info['interfaces'] = interfaces
        
        # Extract TypeScript type definitions
        type_pattern = r'type\s+(\w+)\s*=\s*[^;]+'
        types = re.findall(type_pattern, content)
        info['types'] = types
        
        # Extract exports
        export_patterns = [
            r'export\s+default\s+(?:class\s+|function\s+|const\s+|let\s+|var\s+)?(\w+)',
            r'export\s+(?:const\s+|let\s+|var\s+|function\s+|class\s+)(\w+)',
            r'export\s*\{\s*([^}]+)\s*\}'
        ]
        for pattern in export_patterns:
            exports = re.findall(pattern, content)
            info['exports'].extend(exports)
        
        return info
    except Exception as e:
        return {'error': str(e), 'filepath': filepath}

def extract_generic_info(filepath: str) -> Dict[str, Any]:
    """Extract basic info from other file types"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'size': len(content),
            'lines': len(content.split('\n')),
            'type': 'text'
        }
    except Exception:
        return {'type': 'binary', 'size': os.path.getsize(filepath)}

def load_gitignore_patterns(root_dir: str) -> Set[str]:
    """Load .gitignore patterns"""
    gitignore_patterns = set()
    gitignore_path = os.path.join(root_dir, '.gitignore')
    
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        gitignore_patterns.add(line)
        except Exception:
            pass
    
    return gitignore_patterns

def should_ignore_path(path: str, ignore_patterns: Set[str]) -> bool:
    """Check if path should be ignored based on patterns"""
    path_parts = Path(path).parts
    
    for pattern in ignore_patterns:
        if pattern in path_parts:
            return True
        if any(part.startswith('.') and part != '.' for part in path_parts):
            if pattern.startswith('.'):
                return True
    
    return False

def generate_project_index(root_dir: str = ".") -> Dict[str, Any]:
    """Generate comprehensive project index"""
    start_time = time.time()
    
    index = {
        'project_root': os.path.abspath(root_dir),
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'files': {},
        'summary': {
            'total_files': 0,
            'analyzed_files': 0,
            'languages': {},
            'directories': 0,
            'total_functions': 0,
            'total_classes': 0,
            'generation_time_seconds': 0
        }
    }
    
    # File extensions to analyze
    extractors = {
        '.py': extract_python_info,
        '.js': extract_js_info,
        '.jsx': extract_js_info,
        '.ts': extract_js_info,
        '.tsx': extract_js_info,
        '.vue': extract_js_info,
    }
    
    # Load ignore patterns
    gitignore_patterns = load_gitignore_patterns(root_dir)
    
    # Common patterns to ignore
    default_ignore_patterns = {
        'node_modules', '.git', '__pycache__', '.pytest_cache',
        'dist', 'build', '.venv', 'venv', '.env', '.DS_Store',
        'coverage', '.nyc_output', '.next', '.nuxt', 'out',
        'target', 'bin', 'obj', '.idea', '.vscode'
    }
    
    all_ignore_patterns = gitignore_patterns | default_ignore_patterns
    
    # Walk directory tree
    for root, dirs, files in os.walk(root_dir):
        # Filter directories
        dirs[:] = [d for d in dirs if not should_ignore_path(os.path.join(root, d), all_ignore_patterns)]
        
        rel_root = os.path.relpath(root, root_dir)
        if rel_root != '.':
            index['summary']['directories'] += 1
        
        for file in files:
            if should_ignore_path(os.path.join(root, file), all_ignore_patterns):
                continue
            
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
            
            # Skip if file is too large (>1MB)
            try:
                if os.path.getsize(filepath) > 1024 * 1024:
                    continue
            except OSError:
                continue
            
            # Get file extension
            _, ext = os.path.splitext(file)
            
            # Track language stats
            if ext:
                index['summary']['languages'][ext] = index['summary']['languages'].get(ext, 0) + 1
            
            # Extract file info for supported languages
            if ext in extractors:
                file_info = extractors[ext](filepath)
                if 'error' not in file_info:
                    file_info['path'] = rel_path
                    file_info['size'] = os.path.getsize(filepath)
                    file_info['modified'] = os.path.getmtime(filepath)
                    index['files'][rel_path] = file_info
                    index['summary']['analyzed_files'] += 1
                    
                    # Update summary stats
                    if 'functions' in file_info:
                        index['summary']['total_functions'] += len(file_info['functions'])
                    if 'classes' in file_info:
                        index['summary']['total_classes'] += len(file_info['classes'])
            
            index['summary']['total_files'] += 1
    
    # Calculate generation time
    index['summary']['generation_time_seconds'] = round(time.time() - start_time, 2)
    
    return index

def main():
    """Main entry point for CLI usage"""
    try:
        # Support command line arguments for root directory
        root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
        
        print("🔄 Generating PROJECT_INDEX.json...", file=sys.stderr)
        index = generate_project_index(root_dir)
        
        # Write to PROJECT_INDEX.json
        output_path = "PROJECT_INDEX.json"
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(index, f, indent=2, default=str)
        
        print(f"✅ Generated PROJECT_INDEX.json", file=sys.stderr)
        print(f"📊 Stats: {index['summary']['analyzed_files']} analyzed, {index['summary']['total_functions']} functions, {index['summary']['total_classes']} classes", file=sys.stderr)
        print(f"⏱️  Time: {index['summary']['generation_time_seconds']}s", file=sys.stderr)
        
        # Output JSON for hook consumption
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"PROJECT_INDEX.json updated - {index['summary']['analyzed_files']} files analyzed in {index['summary']['generation_time_seconds']}s"
            }
        }))
        
    except Exception as e:
        print(f"❌ Error generating project index: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()