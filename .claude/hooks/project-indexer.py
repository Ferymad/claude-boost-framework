#!/usr/bin/env python3
"""
Project Index Generator for Claude Code - Performance Optimized
Creates minified abstractions of codebase for project awareness
Prevents code duplication by providing comprehensive project structure overview

Performance Optimizations:
- Caching and memoization for repeated operations
- Parallel processing for large codebases
- Optimized regex patterns with compilation
- Memory-efficient AST traversal
- Incremental updates with change detection
"""
import json
import os
import ast
import re
import sys
import time
import hashlib
import pickle
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache

# Compiled regex patterns for better performance
COMPILED_PATTERNS = {
    'js_import_patterns': [
        re.compile(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'),
        re.compile(r'import\s*\{\s*([^}]+)\s*\}\s*from\s+[\'"]([^\'"]+)[\'"]'),
        re.compile(r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]')
    ],
    'js_func_patterns': [
        re.compile(r'function\s+(\w+)\s*\([^)]*\)'),
        re.compile(r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{'),
        re.compile(r'(\w+)\s*:\s*(?:async\s+)?function\s*\([^)]*\)'),
        re.compile(r'async\s+function\s+(\w+)\s*\([^)]*\)')
    ],
    'js_class_pattern': re.compile(r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'),
    'js_interface_pattern': re.compile(r'interface\s+(\w+)(?:\s+extends\s+[\w,\s]+)?\s*\{'),
    'js_type_pattern': re.compile(r'type\s+(\w+)\s*=\s*[^;]+'),
    'js_export_patterns': [
        re.compile(r'export\s+default\s+(?:class\s+|function\s+|const\s+|let\s+|var\s+)?(\w+)'),
        re.compile(r'export\s+(?:const\s+|let\s+|var\s+|function\s+|class\s+)(\w+)'),
        re.compile(r'export\s*\{\s*([^}]+)\s*\}')
    ]
}

class FileCache:
    """Caches file processing results based on file modification time"""
    
    def __init__(self, cache_dir: str = '.claude/cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_file = os.path.join(cache_dir, 'project_index_cache.pkl')
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache from disk"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception:
            pass
    
    def get_file_hash(self, filepath: str) -> str:
        """Get file content hash for change detection"""
        try:
            stat = os.stat(filepath)
            # Use mtime and size as a fast fingerprint
            return f"{stat.st_mtime}_{stat.st_size}"
        except OSError:
            return ""
    
    def get_cached_result(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Get cached result if file hasn't changed"""
        current_hash = self.get_file_hash(filepath)
        if filepath in self.cache:
            cached_hash, cached_result = self.cache[filepath]
            if cached_hash == current_hash:
                return cached_result
        return None
    
    def set_cached_result(self, filepath: str, result: Dict[str, Any]):
        """Cache the processing result"""
        current_hash = self.get_file_hash(filepath)
        self.cache[filepath] = (current_hash, result)
    
    def save_and_cleanup(self):
        """Save cache and clean up old entries"""
        # Remove entries for files that no longer exist
        to_remove = []
        for filepath in self.cache:
            if not os.path.exists(filepath):
                to_remove.append(filepath)
        
        for filepath in to_remove:
            del self.cache[filepath]
        
        self._save_cache()

# Global cache instance
_file_cache = FileCache()

@lru_cache(maxsize=1024)
def get_file_extension_info(ext: str) -> Tuple[str, bool]:
    """Cached file extension categorization"""
    language_map = {
        '.py': ('python', True),
        '.js': ('javascript', True), 
        '.jsx': ('javascript', True),
        '.ts': ('typescript', True),
        '.tsx': ('typescript', True),
        '.vue': ('vue', True),
        '.java': ('java', True),
        '.c': ('c', True),
        '.cpp': ('cpp', True),
        '.cs': ('csharp', True),
        '.rb': ('ruby', True),
        '.php': ('php', True),
        '.go': ('go', True),
        '.rs': ('rust', True),
        '.swift': ('swift', True),
        '.kt': ('kotlin', True),
        '.scala': ('scala', True),
        '.md': ('markdown', False),
        '.txt': ('text', False),
        '.json': ('json', False),
        '.xml': ('xml', False),
        '.html': ('html', False),
        '.css': ('css', False),
        '.yml': ('yaml', False),
        '.yaml': ('yaml', False)
    }
    return language_map.get(ext, ('unknown', False))

def extract_python_info(filepath: str) -> Dict[str, Any]:
    """Extract imports, functions, classes from Python files - optimized"""
    # Check cache first
    cached_result = _file_cache.get_cached_result(filepath)
    if cached_result is not None:
        return cached_result
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Early exit for empty files
        if not content.strip():
            result = {'imports': [], 'functions': [], 'classes': [], 'constants': [], 'exports': []}
            _file_cache.set_cached_result(filepath, result)
            return result
        
        tree = ast.parse(content)
        info = {
            'imports': [],
            'functions': [],
            'classes': [],
            'constants': [],
            'exports': []
        }
        
        # Use optimized traversal - process top-level nodes directly instead of walking entire tree
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    info['imports'].append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names]
                info['imports'].append(f"from {module} import {', '.join(names)}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
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
                # Process class methods more efficiently
                methods = []
                for n in node.body:
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append({
                            'name': n.name,
                            'args': [arg.arg for arg in n.args.args],
                            'line': n.lineno
                        })
                
                info['classes'].append({
                    'name': node.name,
                    'methods': methods,
                    'line': node.lineno,
                    'bases': [ast.unparse(base) for base in node.bases] if node.bases else []
                })
            elif isinstance(node, ast.Assign):
                # Only check constant assignments at module level
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        info['constants'].append(target.id)
        
        # Cache the result
        _file_cache.set_cached_result(filepath, info)
        return info
    except Exception as e:
        error_result = {'error': str(e), 'filepath': filepath}
        return error_result

def extract_js_info(filepath: str) -> Dict[str, Any]:
    """Extract basic info from JavaScript/TypeScript files - optimized"""
    # Check cache first
    cached_result = _file_cache.get_cached_result(filepath)
    if cached_result is not None:
        return cached_result
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Early exit for empty files
        if not content.strip():
            result = {'imports': [], 'exports': [], 'functions': [], 'classes': [], 'interfaces': [], 'types': []}
            _file_cache.set_cached_result(filepath, result)
            return result
        
        info = {
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': [],
            'interfaces': [],
            'types': []
        }
        
        # Use compiled patterns for better performance
        # Extract imports (ES6 modules)
        for pattern in COMPILED_PATTERNS['js_import_patterns']:
            matches = pattern.findall(content)
            info['imports'].extend(matches)
        
        # Extract function definitions using compiled patterns
        for pattern in COMPILED_PATTERNS['js_func_patterns']:
            functions = pattern.findall(content)
            info['functions'].extend(functions)
        
        # Remove duplicates while preserving order
        info['functions'] = list(dict.fromkeys(info['functions']))
        
        # Extract class definitions
        classes = COMPILED_PATTERNS['js_class_pattern'].findall(content)
        for class_match in classes:
            class_name = class_match[0]
            extends = class_match[1] if class_match[1] else None
            # Simplified method extraction (avoid expensive nested regex)
            info['classes'].append({
                'name': class_name,
                'extends': extends,
                'methods': []  # Skip method extraction for performance
            })
        
        # Extract TypeScript interfaces
        interfaces = COMPILED_PATTERNS['js_interface_pattern'].findall(content)
        info['interfaces'] = interfaces
        
        # Extract TypeScript type definitions
        types = COMPILED_PATTERNS['js_type_pattern'].findall(content)
        info['types'] = types
        
        # Extract exports using compiled patterns
        for pattern in COMPILED_PATTERNS['js_export_patterns']:
            exports = pattern.findall(content)
            info['exports'].extend(exports)
        
        # Remove duplicates
        info['exports'] = list(dict.fromkeys(info['exports']))
        
        # Cache the result
        _file_cache.set_cached_result(filepath, info)
        return info
    except Exception as e:
        error_result = {'error': str(e), 'filepath': filepath}
        return error_result

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

def process_file_parallel(args: Tuple[str, str, Dict]) -> Tuple[str, Optional[Dict[str, Any]]]:
    """Process a single file for parallel execution"""
    filepath, rel_path, extractors = args
    
    try:
        # Skip if file is too large (>1MB)
        file_size = os.path.getsize(filepath)
        if file_size > 1024 * 1024:
            return rel_path, None
        
        # Get file extension
        _, ext = os.path.splitext(filepath)
        
        # Extract file info for supported languages
        if ext in extractors:
            file_info = extractors[ext](filepath)
            if 'error' not in file_info:
                file_info['path'] = rel_path
                file_info['size'] = file_size
                file_info['modified'] = os.path.getmtime(filepath)
                return rel_path, file_info
        
        return rel_path, None
    except Exception:
        return rel_path, None

def generate_project_index(root_dir: str = ".", max_workers: int = 4) -> Dict[str, Any]:
    """Generate comprehensive project index - optimized with parallel processing"""
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
            'cached_files': 0,
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
    
    # Load ignore patterns with caching
    gitignore_patterns = load_gitignore_patterns(root_dir)
    
    # Optimized ignore patterns - convert to set for O(1) lookup
    default_ignore_patterns = {
        'node_modules', '.git', '__pycache__', '.pytest_cache',
        'dist', 'build', '.venv', 'venv', '.env', '.DS_Store',
        'coverage', '.nyc_output', '.next', '.nuxt', 'out',
        'target', 'bin', 'obj', '.idea', '.vscode', '.claude'
    }
    
    all_ignore_patterns = gitignore_patterns | default_ignore_patterns
    
    # Collect files to process
    files_to_process = []
    
    # Walk directory tree once to collect files
    for root, dirs, files in os.walk(root_dir):
        # Filter directories efficiently
        dirs[:] = [d for d in dirs if not should_ignore_path(os.path.join(root, d), all_ignore_patterns)]
        
        rel_root = os.path.relpath(root, root_dir)
        if rel_root != '.':
            index['summary']['directories'] += 1
        
        for file in files:
            if should_ignore_path(os.path.join(root, file), all_ignore_patterns):
                continue
            
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
            
            # Get file extension for language stats
            _, ext = os.path.splitext(file)
            if ext:
                index['summary']['languages'][ext] = index['summary']['languages'].get(ext, 0) + 1
            
            # Only queue supported files for processing
            if ext in extractors:
                files_to_process.append((filepath, rel_path, extractors))
            
            index['summary']['total_files'] += 1
    
    # Process files in parallel for better performance
    if files_to_process and len(files_to_process) > 2:
        # Use ThreadPoolExecutor for I/O bound operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(process_file_parallel, files_to_process)
    else:
        # Single-threaded for small projects
        results = map(process_file_parallel, files_to_process)
    
    # Collect results
    for rel_path, file_info in results:
        if file_info is not None:
            index['files'][rel_path] = file_info
            index['summary']['analyzed_files'] += 1
            
            # Update summary stats efficiently
            if 'functions' in file_info:
                index['summary']['total_functions'] += len(file_info['functions'])
            if 'classes' in file_info:
                index['summary']['total_classes'] += len(file_info['classes'])
    
    # Track cache efficiency
    index['summary']['cached_files'] = _file_cache.cache.__len__()
    
    # Calculate generation time
    index['summary']['generation_time_seconds'] = round(time.time() - start_time, 2)
    
    # Save and cleanup cache
    _file_cache.save_and_cleanup()
    
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