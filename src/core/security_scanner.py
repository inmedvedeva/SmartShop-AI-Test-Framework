"""
Security scanning utilities for SmartShop AI Test Framework
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from src.core.constants import REPORT_DIR


class SecurityScanner:
    """Security scanning utilities"""

    def __init__(self, report_dir: str = REPORT_DIR):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)

    def run_bandit_scan(
        self, target_path: str = ".", output_file: str = "bandit_report.json"
    ) -> dict[str, Any]:
        """Run Bandit security scan"""
        try:
            cmd = [
                sys.executable,
                "-m",
                "bandit",
                "-r",
                target_path,
                "-f",
                "json",
                "-o",
                str(self.report_dir / output_file),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                logger.info("Bandit scan completed successfully")
            else:
                logger.warning(f"Bandit scan completed with warnings: {result.stderr}")

            # Read the report
            report_path = self.report_dir / output_file
            if report_path.exists():
                with open(report_path) as f:
                    report = json.load(f)

                # Add scan metadata
                report["scan_metadata"] = {
                    "tool": "bandit",
                    "target": target_path,
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }

                logger.info(f"Bandit scan report saved: {report_path}")
                return report
            else:
                logger.error("Bandit report file not found")
                return {"error": "Report file not found"}

        except subprocess.TimeoutExpired:
            logger.error("Bandit scan timed out")
            return {"error": "Scan timed out"}
        except Exception as e:
            logger.error(f"Error running Bandit scan: {e}")
            return {"error": str(e)}

    def run_safety_scan(
        self, output_file: str = "safety_report.json"
    ) -> dict[str, Any]:
        """Run Safety security scan"""
        try:
            cmd = [
                sys.executable,
                "-m",
                "safety",
                "check",
                "--json",
                "--output",
                str(self.report_dir / output_file),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                logger.info("Safety scan completed successfully")
            else:
                logger.warning(f"Safety scan completed with warnings: {result.stderr}")

            # Read the report
            report_path = self.report_dir / output_file
            if report_path.exists():
                with open(report_path) as f:
                    report = json.load(f)

                # Add scan metadata
                report["scan_metadata"] = {
                    "tool": "safety",
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }

                logger.info(f"Safety scan report saved: {report_path}")
                return report
            else:
                logger.error("Safety report file not found")
                return {"error": "Report file not found"}

        except subprocess.TimeoutExpired:
            logger.error("Safety scan timed out")
            return {"error": "Scan timed out"}
        except Exception as e:
            logger.error(f"Error running Safety scan: {e}")
            return {"error": str(e)}

    def run_semgrep_scan(
        self, target_path: str = ".", output_file: str = "semgrep_report.json"
    ) -> dict[str, Any]:
        """Run Semgrep security scan"""
        try:
            cmd = [
                "semgrep",
                "--json",
                "--output",
                str(self.report_dir / output_file),
                target_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

            if result.returncode == 0:
                logger.info("Semgrep scan completed successfully")
            else:
                logger.warning(f"Semgrep scan completed with warnings: {result.stderr}")

            # Read the report
            report_path = self.report_dir / output_file
            if report_path.exists():
                with open(report_path) as f:
                    report = json.load(f)

                # Add scan metadata
                report["scan_metadata"] = {
                    "tool": "semgrep",
                    "target": target_path,
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }

                logger.info(f"Semgrep scan report saved: {report_path}")
                return report
            else:
                logger.error("Semgrep report file not found")
                return {"error": "Report file not found"}

        except subprocess.TimeoutExpired:
            logger.error("Semgrep scan timed out")
            return {"error": "Scan timed out"}
        except FileNotFoundError:
            logger.warning("Semgrep not installed, skipping scan")
            return {"error": "Semgrep not installed"}
        except Exception as e:
            logger.error(f"Error running Semgrep scan: {e}")
            return {"error": str(e)}

    def run_comprehensive_scan(self, target_path: str = ".") -> dict[str, Any]:
        """Run comprehensive security scan with all tools"""
        logger.info("Starting comprehensive security scan")

        results = {
            "scan_timestamp": str(Path().stat().st_mtime),
            "target_path": target_path,
            "tools": {},
        }

        # Run Bandit scan
        logger.info("Running Bandit scan...")
        results["tools"]["bandit"] = self.run_bandit_scan(target_path)

        # Run Safety scan
        logger.info("Running Safety scan...")
        results["tools"]["safety"] = self.run_safety_scan()

        # Run Semgrep scan (if available)
        logger.info("Running Semgrep scan...")
        results["tools"]["semgrep"] = self.run_semgrep_scan(target_path)

        # Generate summary
        results["summary"] = self._generate_scan_summary(results["tools"])

        # Save comprehensive report
        comprehensive_report_path = (
            self.report_dir / "comprehensive_security_report.json"
        )
        with open(comprehensive_report_path, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"Comprehensive security report saved: {comprehensive_report_path}")
        return results

    def _generate_scan_summary(self, tool_results: dict[str, Any]) -> dict[str, Any]:
        """Generate summary from scan results"""
        summary = {
            "total_issues": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "tools_used": [],
            "tools_failed": [],
        }

        for tool_name, result in tool_results.items():
            if "error" in result:
                summary["tools_failed"].append(tool_name)
                continue

            summary["tools_used"].append(tool_name)

            # Count issues based on tool
            if tool_name == "bandit" and "results" in result:
                for issue in result["results"]:
                    summary["total_issues"] += 1
                    severity = issue.get("issue_severity", "low").lower()
                    if severity == "high":
                        summary["high_severity"] += 1
                    elif severity == "medium":
                        summary["medium_severity"] += 1
                    else:
                        summary["low_severity"] += 1

            elif tool_name == "safety" and isinstance(result, list):
                for issue in result:
                    summary["total_issues"] += 1
                    severity = issue.get("severity", "low").lower()
                    if severity == "high":
                        summary["high_severity"] += 1
                    elif severity == "medium":
                        summary["medium_severity"] += 1
                    else:
                        summary["low_severity"] += 1

            elif tool_name == "semgrep" and "results" in result:
                for issue in result["results"]:
                    summary["total_issues"] += 1
                    severity = issue.get("extra", {}).get("severity", "low").lower()
                    if severity == "error":
                        summary["high_severity"] += 1
                    elif severity == "warning":
                        summary["medium_severity"] += 1
                    else:
                        summary["low_severity"] += 1

        return summary

    def check_security_thresholds(
        self,
        scan_results: dict[str, Any],
        max_high: int = 0,
        max_medium: int = 5,
        max_low: int = 10,
    ) -> dict[str, Any]:
        """Check if security scan results meet thresholds"""
        summary = scan_results.get("summary", {})

        high_count = summary.get("high_severity", 0)
        medium_count = summary.get("medium_severity", 0)
        low_count = summary.get("low_severity", 0)

        thresholds_met = {
            "high_severity": high_count <= max_high,
            "medium_severity": medium_count <= max_medium,
            "low_severity": low_count <= max_low,
            "overall": (
                high_count <= max_high
                and medium_count <= max_medium
                and low_count <= max_low
            ),
        }

        result = {
            "thresholds_met": thresholds_met,
            "current_counts": {
                "high": high_count,
                "medium": medium_count,
                "low": low_count,
            },
            "thresholds": {
                "max_high": max_high,
                "max_medium": max_medium,
                "max_low": max_low,
            },
        }

        if not thresholds_met["overall"]:
            logger.warning("Security thresholds not met")
            if not thresholds_met["high_severity"]:
                logger.error(
                    f"High severity issues exceed threshold: {high_count} > {max_high}"
                )
            if not thresholds_met["medium_severity"]:
                logger.warning(
                    f"Medium severity issues exceed threshold: {medium_count} > {max_medium}"
                )
            if not thresholds_met["low_severity"]:
                logger.warning(
                    f"Low severity issues exceed threshold: {low_count} > {max_low}"
                )
        else:
            logger.info("All security thresholds met")

        return result


def get_security_scanner() -> SecurityScanner:
    """Factory function to get security scanner"""
    return SecurityScanner()
