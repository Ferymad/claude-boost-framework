#!/usr/bin/env python3
"""
Claude Boost Installation Verification Script
Validates that all components are correctly installed and functional
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class InstallationVerifier:
    """Comprehensive installation verification for Claude Boost"""
    
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log_result(self, test_name: str, status: str, message: str, details: Optional[str] = None):
        """Log test result with timestamp"""
        result = {
            'test': test_name,
            'status': status,  # PASS, FAIL, WARN, SKIP
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        icon = {
            'PASS': '✅',
            'FAIL': '❌', 
            'WARN': '⚠️',
            'SKIP': '⏭️'
        }.get(status, '❓')
        
        print(f"{icon} {test_name}: {status} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def run_command(self, cmd: List[str], cwd: Optional[str] = None, timeout: int = 30) -> Tuple[bool, str, str]:
        """Run command and return success, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd,
                capture_output=True, 
                text=True, 
                timeout=timeout,
                check=False
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout}s"
        except Exception as e:
            return False, "", str(e)
    
    def check_system_requirements(self):
        """Check system prerequisites"""
        print("\n🔍 Checking System Requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.log_result(
                "Python Version",
                "PASS", 
                f"Python {python_version.major}.{python_version.minor}.{python_version.micro}"
            )
        else:
            self.log_result(
                "Python Version", 
                "FAIL",
                f"Python {python_version.major}.{python_version.minor} < 3.8 (minimum required)"
            )
        
        # Check Node.js
        success, stdout, stderr = self.run_command(['node', '--version'])
        if success:
            version = stdout.strip()
            self.log_result("Node.js", "PASS", f"Node.js {version}")
        else:
            self.log_result("Node.js", "WARN", "Node.js not available", stderr)
        
        # Check npm
        success, stdout, stderr = self.run_command(['npm', '--version'])
        if success:
            version = stdout.strip() 
            self.log_result("npm", "PASS", f"npm {version}")
        else:
            self.log_result("npm", "WARN", "npm not available", stderr)
        
        # Check git
        success, stdout, stderr = self.run_command(['git', '--version'])
        if success:
            version = stdout.strip()
            self.log_result("Git", "PASS", version)
        else:
            self.log_result("Git", "WARN", "Git not available", stderr)
    
    def verify_npm_package(self, package_path: str):
        """Verify NPM package structure and contents"""
        print("\n📦 Verifying NPM Package...")
        
        package_dir = Path(package_path)
        if not package_dir.exists():
            self.log_result("Package Directory", "FAIL", f"Directory {package_path} not found")
            return
        
        # Check package.json
        package_json_path = package_dir / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                # Verify required fields
                required_fields = ['name', 'version', 'main', 'bin']
                missing_fields = [field for field in required_fields if field not in package_data]
                
                if not missing_fields:
                    self.log_result(
                        "Package.json Structure", 
                        "PASS",
                        f"All required fields present (name: {package_data.get('name')}, version: {package_data.get('version')})"
                    )
                else:
                    self.log_result(
                        "Package.json Structure",
                        "FAIL", 
                        f"Missing required fields: {', '.join(missing_fields)}"
                    )
                
                # Check beta configuration
                if package_data.get('publishConfig', {}).get('tag') == 'beta':
                    self.log_result("Beta Configuration", "PASS", "Package configured for beta release")
                else:
                    self.log_result("Beta Configuration", "WARN", "Package not configured for beta release")
                    
            except json.JSONDecodeError as e:
                self.log_result("Package.json Parsing", "FAIL", f"Invalid JSON: {e}")
        else:
            self.log_result("Package.json Existence", "FAIL", "package.json not found")
        
        # Check main entry point
        main_file = package_dir / "claude_boost" / "cli.js"
        if main_file.exists():
            self.log_result("Main Entry Point", "PASS", "cli.js found")
        else:
            self.log_result("Main Entry Point", "FAIL", "cli.js not found")
        
        # Check Python CLI
        python_cli = package_dir / "claude_boost" / "cli.py"
        if python_cli.exists():
            self.log_result("Python CLI", "PASS", "Python CLI found")
        else:
            self.log_result("Python CLI", "FAIL", "Python CLI not found")
    
    def verify_template_files(self, package_path: str):
        """Verify all template files are present"""
        print("\n📄 Verifying Template Files...")
        
        templates_dir = Path(package_path) / "claude_boost" / "templates" / ".claude"
        if not templates_dir.exists():
            self.log_result("Templates Directory", "FAIL", "Templates directory not found")
            return
        
        # Required template files
        required_templates = {
            'agents': ['blind-validator.md', 'code-reviewer.md', 'debugger.md', 'test-runner.md'],
            'commands': ['cleanup.md', 'fresh.md', 'validate.md'],
            'hooks': ['project-indexer.py', 'session-manager.py']
        }
        
        total_templates = 0
        missing_templates = []
        
        for category, files in required_templates.items():
            category_dir = templates_dir / category
            if category_dir.exists():
                for filename in files:
                    template_path = category_dir / filename
                    if template_path.exists():
                        total_templates += 1
                    else:
                        missing_templates.append(f"{category}/{filename}")
            else:
                missing_templates.extend([f"{category}/{file}" for file in files])
        
        if not missing_templates:
            self.log_result(
                "Template Files",
                "PASS", 
                f"All {total_templates} required template files present"
            )
        else:
            self.log_result(
                "Template Files", 
                "FAIL",
                f"Missing {len(missing_templates)} templates: {', '.join(missing_templates)}"
            )
        
        # Check CLAUDE.md template
        claude_md = templates_dir / "CLAUDE.md"
        if claude_md.exists():
            self.log_result("CLAUDE.md Template", "PASS", "Main template found")
        else:
            self.log_result("CLAUDE.md Template", "FAIL", "Main template not found")
    
    def test_npm_pack(self, package_path: str):
        """Test npm pack functionality"""
        print("\n📦 Testing NPM Pack...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run npm pack
            success, stdout, stderr = self.run_command(['npm', 'pack'], cwd=package_path)
            
            if success:
                # Find the generated tarball
                tarballs = list(Path(package_path).glob('*.tgz'))
                if tarballs:
                    tarball = tarballs[0]
                    size_mb = tarball.stat().st_size / (1024 * 1024)
                    self.log_result(
                        "NPM Pack",
                        "PASS",
                        f"Package created: {tarball.name} ({size_mb:.2f} MB)"
                    )
                    
                    # Move to temp dir for testing
                    temp_tarball = Path(temp_dir) / tarball.name
                    shutil.move(str(tarball), str(temp_tarball))
                    
                    # Test installation from tarball
                    install_dir = Path(temp_dir) / "test_install"
                    install_dir.mkdir()
                    
                    success, stdout, stderr = self.run_command([
                        'npm', 'install', str(temp_tarball), '--prefix', str(install_dir)
                    ])
                    
                    if success:
                        self.log_result("Tarball Installation", "PASS", "Installation from tarball successful")
                    else:
                        self.log_result("Tarball Installation", "FAIL", "Installation failed", stderr)
                        
                else:
                    self.log_result("NPM Pack", "FAIL", "No tarball generated")
            else:
                self.log_result("NPM Pack", "FAIL", "npm pack failed", stderr)
    
    def test_python_setup(self, package_path: str):
        """Test Python package setup"""
        print("\n🐍 Testing Python Setup...")
        
        # Check setup.py exists
        setup_py = Path(package_path) / "setup.py"
        if not setup_py.exists():
            self.log_result("Setup.py", "FAIL", "setup.py not found")
            return
        
        # Test setup.py check
        success, stdout, stderr = self.run_command(
            [sys.executable, 'setup.py', 'check'], 
            cwd=package_path
        )
        
        if success:
            self.log_result("Setup.py Check", "PASS", "Setup configuration valid")
        else:
            self.log_result("Setup.py Check", "FAIL", "Setup check failed", stderr)
        
        # Test setup.py sdist (source distribution)
        with tempfile.TemporaryDirectory() as temp_dir:
            success, stdout, stderr = self.run_command([
                sys.executable, 'setup.py', 'sdist', '--dist-dir', temp_dir
            ], cwd=package_path)
            
            if success:
                dist_files = list(Path(temp_dir).glob('*.tar.gz'))
                if dist_files:
                    size_kb = dist_files[0].stat().st_size / 1024
                    self.log_result(
                        "Python Source Distribution",
                        "PASS",
                        f"Source package created: {dist_files[0].name} ({size_kb:.1f} KB)"
                    )
                else:
                    self.log_result("Python Source Distribution", "FAIL", "No distribution file created")
            else:
                self.log_result("Python Source Distribution", "FAIL", "sdist failed", stderr)
    
    def generate_report(self) -> Dict:
        """Generate comprehensive test report"""
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        warnings = sum(1 for r in self.results if r['status'] == 'WARN')
        skipped = sum(1 for r in self.results if r['status'] == 'SKIP')
        
        report = {
            'timestamp': self.timestamp,
            'platform': f"{sys.platform} ({os.name})",
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'summary': {
                'total_tests': len(self.results),
                'passed': passed,
                'failed': failed,
                'warnings': warnings,
                'skipped': skipped,
                'success_rate': f"{(passed / len(self.results) * 100):.1f}%" if self.results else "0%"
            },
            'results': self.results
        }
        
        return report
    
    def save_report(self, report: Dict, output_dir: str = "test-installation/logs"):
        """Save report to JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        report_file = Path(output_dir) / f"verification_report_{self.timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Report saved to: {report_file}")
        return report_file


def main():
    """Main verification function"""
    print("🧪 Claude Boost Installation Verification")
    print("==========================================")
    
    verifier = InstallationVerifier()
    
    # Determine package path
    package_path = "claude-boost"
    if len(sys.argv) > 1:
        package_path = sys.argv[1]
    
    if not os.path.exists(package_path):
        print(f"❌ Package directory '{package_path}' not found")
        print("Usage: python verify_installation.py [package_path]")
        sys.exit(1)
    
    print(f"Package path: {os.path.abspath(package_path)}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()
    
    # Run all verification tests
    try:
        verifier.check_system_requirements()
        verifier.verify_npm_package(package_path)
        verifier.verify_template_files(package_path)
        verifier.test_npm_pack(package_path)
        verifier.test_python_setup(package_path)
        
    except KeyboardInterrupt:
        print("\n⏹️ Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during verification: {e}")
        sys.exit(1)
    
    # Generate and save report
    report = verifier.generate_report()
    report_file = verifier.save_report(report)
    
    # Print summary
    print(f"\n📊 Verification Summary")
    print("=" * 50)
    print(f"Total tests: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Success rate: {report['summary']['success_rate']}")
    
    # Exit with appropriate code
    if report['summary']['failed'] > 0:
        print("\n❌ Some tests failed. Package needs attention before release.")
        sys.exit(1)
    elif report['summary']['warnings'] > 0:
        print("\n⚠️ All tests passed with warnings. Review recommended.")
        sys.exit(0)
    else:
        print("\n✅ All tests passed! Package is ready for beta release.")
        sys.exit(0)


if __name__ == "__main__":
    main()