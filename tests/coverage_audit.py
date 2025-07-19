"""
Test Coverage Audit Script
Analyzes the project structure and provides recommendations for improving test coverage
"""

import ast
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


class CoverageAuditor:
    """Audits test coverage and provides recommendations"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.python_files = []
        self.test_files = []
        self.source_files = []
        self.coverage_data = {}

    def scan_project(self) -> dict:
        """Scan the entire project structure"""
        print("🔍 Scanning project structure...")

        # Find all Python files
        for root, dirs, files in os.walk(self.project_root):
            # Skip virtual environment and cache directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["venv", "__pycache__", ".pytest_cache"]
            ]

            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    self.python_files.append(file_path)

                    if "test" in file.lower() or file.startswith("test_"):
                        self.test_files.append(file_path)
                    else:
                        self.source_files.append(file_path)

        return {
            "total_python_files": len(self.python_files),
            "test_files": len(self.test_files),
            "source_files": len(self.source_files),
            "test_ratio": (
                len(self.test_files) / len(self.source_files)
                if self.source_files
                else 0
            ),
        }

    def analyze_test_structure(self) -> dict:
        """Analyze test file structure and organization"""
        print("📊 Analyzing test structure...")

        test_categories = defaultdict(list)
        test_markers = defaultdict(int)
        test_functions = defaultdict(int)

        for test_file in self.test_files:
            relative_path = test_file.relative_to(self.project_root)

            # Categorize by directory
            if "ui" in str(relative_path):
                test_categories["ui"].append(test_file)
            elif "api" in str(relative_path):
                test_categories["api"].append(test_file)
            elif "integration" in str(relative_path):
                test_categories["integration"].append(test_file)
            elif "performance" in str(relative_path):
                test_categories["performance"].append(test_file)
            elif "unit" in str(relative_path):
                test_categories["unit"].append(test_file)
            else:
                test_categories["other"].append(test_file)

            # Analyze test content
            try:
                with open(test_file, encoding="utf-8") as f:
                    content = f.read()

                    # Count test functions
                    test_func_count = len(re.findall(r"def test_", content))
                    test_functions[str(relative_path)] = test_func_count

                    # Count pytest markers
                    markers = re.findall(r"@pytest\.mark\.(\w+)", content)
                    for marker in markers:
                        test_markers[marker] += 1

            except Exception as e:
                print(f"⚠️ Error analyzing {test_file}: {e}")

        return {
            "test_categories": {k: len(v) for k, v in test_categories.items()},
            "test_markers": dict(test_markers),
            "test_functions": dict(test_functions),
            "total_test_functions": sum(test_functions.values()),
        }

    def analyze_source_coverage(self) -> dict:
        """Analyze which source files are covered by tests"""
        print("🎯 Analyzing source code coverage...")

        source_modules = set()
        tested_modules = set()

        # Extract module names from source files
        for source_file in self.source_files:
            relative_path = source_file.relative_to(self.project_root)
            module_name = str(relative_path).replace("/", ".").replace(".py", "")
            source_modules.add(module_name)

        # Check which modules are imported in tests
        for test_file in self.test_files:
            try:
                with open(test_file, encoding="utf-8") as f:
                    content = f.read()

                    # Parse imports
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                tested_modules.add(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                tested_modules.add(node.module)

            except Exception as e:
                print(f"⚠️ Error parsing {test_file}: {e}")

        uncovered_modules = source_modules - tested_modules

        return {
            "total_modules": len(source_modules),
            "tested_modules": len(tested_modules),
            "uncovered_modules": len(uncovered_modules),
            "coverage_percentage": (
                (len(tested_modules) / len(source_modules) * 100)
                if source_modules
                else 0
            ),
            "uncovered_modules_list": list(uncovered_modules),
        }

    def analyze_code_complexity(self) -> dict:
        """Analyze code complexity and identify areas needing more testing"""
        print("🔍 Analyzing code complexity...")

        complex_functions = []
        large_classes = []

        for source_file in self.source_files:
            try:
                with open(source_file, encoding="utf-8") as f:
                    content = f.read()
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            # Count lines in function
                            lines = len(node.body)
                            if lines > 20:  # Function with more than 20 lines
                                complex_functions.append(
                                    {
                                        "file": str(
                                            source_file.relative_to(self.project_root)
                                        ),
                                        "function": node.name,
                                        "lines": lines,
                                        "complexity": "high",
                                    }
                                )

                        elif isinstance(node, ast.ClassDef):
                            # Count methods in class
                            methods = len(
                                [n for n in node.body if isinstance(n, ast.FunctionDef)]
                            )
                            if methods > 10:  # Class with more than 10 methods
                                large_classes.append(
                                    {
                                        "file": str(
                                            source_file.relative_to(self.project_root)
                                        ),
                                        "class": node.name,
                                        "methods": methods,
                                        "complexity": "high",
                                    }
                                )

            except Exception as e:
                print(f"⚠️ Error analyzing complexity in {source_file}: {e}")

        return {
            "complex_functions": complex_functions,
            "large_classes": large_classes,
            "total_complex_functions": len(complex_functions),
            "total_large_classes": len(large_classes),
        }

    def check_missing_test_patterns(self) -> dict:
        """Check for common missing test patterns"""
        print("🔍 Checking for missing test patterns...")

        missing_patterns = {
            "error_handling": [],
            "edge_cases": [],
            "negative_tests": [],
            "boundary_tests": [],
            "integration_tests": [],
            "performance_tests": [],
        }

        # Analyze test files for patterns
        for test_file in self.test_files:
            try:
                with open(test_file, encoding="utf-8") as f:
                    content = f.read().lower()

                    # Check for error handling tests
                    if not any(
                        term in content
                        for term in ["error", "exception", "fail", "invalid"]
                    ):
                        missing_patterns["error_handling"].append(
                            str(test_file.relative_to(self.project_root))
                        )

                    # Check for edge cases
                    if not any(
                        term in content
                        for term in ["edge", "boundary", "limit", "empty", "null"]
                    ):
                        missing_patterns["edge_cases"].append(
                            str(test_file.relative_to(self.project_root))
                        )

                    # Check for negative tests
                    if not any(
                        term in content
                        for term in ["negative", "invalid", "wrong", "incorrect"]
                    ):
                        missing_patterns["negative_tests"].append(
                            str(test_file.relative_to(self.project_root))
                        )

            except Exception as e:
                print(f"⚠️ Error checking patterns in {test_file}: {e}")

        return missing_patterns

    def generate_recommendations(self) -> list[str]:
        """Generate specific recommendations for improving test coverage"""
        print("💡 Generating recommendations...")

        recommendations = []

        # Analyze coverage data
        if (
            self.coverage_data.get("source_coverage", {}).get("coverage_percentage", 0)
            < 80
        ):
            recommendations.append("📈 Increase overall test coverage to at least 80%")

        if self.coverage_data.get("source_coverage", {}).get("uncovered_modules"):
            recommendations.append(
                "🎯 Add tests for uncovered modules: "
                + ", ".join(
                    self.coverage_data["source_coverage"]["uncovered_modules_list"][:5]
                )
            )

        if self.coverage_data.get("complexity", {}).get("complex_functions"):
            recommendations.append(
                "🔧 Add unit tests for complex functions with high cyclomatic complexity"
            )

        if self.coverage_data.get("complexity", {}).get("large_classes"):
            recommendations.append(
                "🏗️ Add integration tests for large classes with many methods"
            )

        # Check test distribution
        test_categories = self.coverage_data.get("test_structure", {}).get(
            "test_categories", {}
        )
        if test_categories.get("unit", 0) < test_categories.get("ui", 0):
            recommendations.append(
                "⚡ Increase unit test coverage - they're faster and more reliable than UI tests"
            )

        if test_categories.get("integration", 0) < 2:
            recommendations.append(
                "🔗 Add more integration tests to verify component interactions"
            )

        if test_categories.get("performance", 0) < 1:
            recommendations.append(
                "⚡ Add performance tests to ensure system scalability"
            )

        # Check for missing patterns
        missing_patterns = self.coverage_data.get("missing_patterns", {})
        if missing_patterns.get("error_handling"):
            recommendations.append(
                "🚨 Add error handling tests for robust error scenarios"
            )

        if missing_patterns.get("negative_tests"):
            recommendations.append(
                "❌ Add negative test cases to verify invalid input handling"
            )

        if missing_patterns.get("edge_cases"):
            recommendations.append("🔍 Add edge case tests for boundary conditions")

        return recommendations

    def run_full_audit(self) -> dict:
        """Run complete coverage audit"""
        print("🚀 Starting comprehensive test coverage audit...\n")

        # Run all analysis steps
        self.coverage_data = {
            "project_structure": self.scan_project(),
            "test_structure": self.analyze_test_structure(),
            "source_coverage": self.analyze_source_coverage(),
            "complexity": self.analyze_code_complexity(),
            "missing_patterns": self.check_missing_test_patterns(),
        }

        # Generate recommendations
        self.coverage_data["recommendations"] = self.generate_recommendations()

        return self.coverage_data

    def print_report(self):
        """Print formatted audit report"""
        print("\n" + "=" * 80)
        print("📊 TEST COVERAGE AUDIT REPORT")
        print("=" * 80)

        # Project Structure
        print("\n🏗️ PROJECT STRUCTURE:")
        structure = self.coverage_data["project_structure"]
        print(f"   Total Python files: {structure['total_python_files']}")
        print(f"   Source files: {structure['source_files']}")
        print(f"   Test files: {structure['test_files']}")
        print(f"   Test ratio: {structure['test_ratio']:.2f}")

        # Test Structure
        print("\n🧪 TEST STRUCTURE:")
        test_structure = self.coverage_data["test_structure"]
        print(f"   Total test functions: {test_structure['total_test_functions']}")
        print("   Test categories:")
        for category, count in test_structure["test_categories"].items():
            print(f"     - {category}: {count}")

        print("   Test markers:")
        for marker, count in test_structure["test_markers"].items():
            print(f"     - @{marker}: {count}")

        # Source Coverage
        print("\n🎯 SOURCE COVERAGE:")
        coverage = self.coverage_data["source_coverage"]
        print(f"   Total modules: {coverage['total_modules']}")
        print(f"   Tested modules: {coverage['tested_modules']}")
        print(f"   Coverage: {coverage['coverage_percentage']:.1f}%")

        if coverage["uncovered_modules_list"]:
            print("   Uncovered modules:")
            for module in coverage["uncovered_modules_list"][:10]:  # Show first 10
                print(f"     - {module}")

        # Complexity Analysis
        print("\n🔍 COMPLEXITY ANALYSIS:")
        complexity = self.coverage_data["complexity"]
        print(f"   Complex functions: {complexity['total_complex_functions']}")
        print(f"   Large classes: {complexity['total_large_classes']}")

        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(self.coverage_data["recommendations"], 1):
            print(f"   {i}. {rec}")

        print("\n" + "=" * 80)
        print("✅ Audit completed!")
        print("=" * 80)

    def save_report(self, filename: str = "coverage_audit_report.json"):
        """Save audit report to JSON file"""
        report_path = self.project_root / "reports" / filename

        # Ensure reports directory exists
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.coverage_data, f, indent=2, default=str)

        print(f"\n📄 Report saved to: {report_path}")


def main():
    """Main function to run the coverage audit"""
    auditor = CoverageAuditor()

    try:
        # Run full audit
        auditor.run_full_audit()

        # Print report
        auditor.print_report()

        # Save report
        auditor.save_report()

    except Exception as e:
        print(f"❌ Error during audit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
