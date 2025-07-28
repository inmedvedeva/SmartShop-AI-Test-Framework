#!/usr/bin/env python3
"""
Cleanup script for test reports and artifacts
"""
import argparse
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from loguru import logger


class ReportCleanup:
    """Cleanup old test reports and artifacts"""

    def __init__(self, project_root: Path = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent

        self.project_root = project_root
        self.reports_dir = project_root / "reports"
        self.screenshots_dir = self.reports_dir / "screenshots"
        self.logs_dir = project_root / "logs"

    def cleanup_old_reports(self, days: int = 7):
        """Clean up reports older than specified days"""
        logger.info(f"Cleaning up reports older than {days} days")

        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0

        # Clean up mobile reports
        mobile_reports_dir = self.reports_dir / "mobile"
        if mobile_reports_dir.exists():
            for report_dir in mobile_reports_dir.iterdir():
                if report_dir.is_dir() and report_dir.name != "latest":
                    try:
                        # Check if directory name is a timestamp
                        dir_date = datetime.strptime(report_dir.name, "%Y%m%d_%H%M%S")
                        if dir_date < cutoff_date:
                            shutil.rmtree(report_dir)
                            logger.info(f"Removed old mobile report: {report_dir.name}")
                            cleaned_count += 1
                    except ValueError:
                        # Not a timestamp directory, skip
                        continue

        # Clean up screenshots
        if self.screenshots_dir.exists():
            for screenshot in self.screenshots_dir.glob("*.png"):
                try:
                    mtime = datetime.fromtimestamp(screenshot.stat().st_mtime)
                    if mtime < cutoff_date:
                        screenshot.unlink()
                        logger.info(f"Removed old screenshot: {screenshot.name}")
                        cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove {screenshot}: {e}")

        # Clean up logs
        if self.logs_dir.exists():
            for log_file in self.logs_dir.glob("*.log*"):
                try:
                    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if mtime < cutoff_date:
                        log_file.unlink()
                        logger.info(f"Removed old log: {log_file.name}")
                        cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove {log_file}: {e}")

        logger.info(f"Cleanup completed: {cleaned_count} items removed")
        return cleaned_count

    def cleanup_empty_directories(self):
        """Remove empty directories"""
        logger.info("Cleaning up empty directories")

        cleaned_count = 0

        for root, dirs, files in os.walk(self.reports_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        logger.info(f"Removed empty directory: {dir_path}")
                        cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove {dir_path}: {e}")

        logger.info(f"Empty directories cleanup completed: {cleaned_count} removed")
        return cleaned_count

    def get_disk_usage(self):
        """Get disk usage of reports directory"""
        if not self.reports_dir.exists():
            return 0

        total_size = 0
        file_count = 0

        for root, dirs, files in os.walk(self.reports_dir):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                    file_count += 1
                except Exception:
                    continue

        return total_size, file_count

    def print_disk_usage(self):
        """Print disk usage information"""
        total_size, file_count = self.get_disk_usage()

        size_mb = total_size / (1024 * 1024)
        logger.info(f"Reports directory usage:")
        logger.info(f"  Total files: {file_count}")
        logger.info(f"  Total size: {size_mb:.2f} MB")

        # Show breakdown by subdirectory
        if self.reports_dir.exists():
            for subdir in self.reports_dir.iterdir():
                if subdir.is_dir():
                    subdir_size = 0
                    subdir_files = 0
                    for root, dirs, files in os.walk(subdir):
                        for file in files:
                            file_path = Path(root) / file
                            try:
                                subdir_size += file_path.stat().st_size
                                subdir_files += 1
                            except Exception:
                                continue

                    subdir_mb = subdir_size / (1024 * 1024)
                    logger.info(
                        f"  {subdir.name}: {subdir_files} files, {subdir_mb:.2f} MB"
                    )

    def cleanup_all(self, days: int = 7):
        """Perform complete cleanup"""
        logger.info("Starting complete cleanup")

        # Print initial disk usage
        self.print_disk_usage()

        # Clean up old reports
        old_reports_cleaned = self.cleanup_old_reports(days)

        # Clean up empty directories
        empty_dirs_cleaned = self.cleanup_empty_directories()

        # Print final disk usage
        logger.info("Cleanup completed. Final disk usage:")
        self.print_disk_usage()

        return {
            "old_reports_cleaned": old_reports_cleaned,
            "empty_dirs_cleaned": empty_dirs_cleaned,
        }


def main():
    """Main function for cleanup script"""
    parser = argparse.ArgumentParser(description="Cleanup test reports and artifacts")

    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Remove reports older than N days (default: 7)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be cleaned without actually removing files",
    )

    parser.add_argument(
        "--disk-usage", action="store_true", help="Show disk usage information only"
    )

    args = parser.parse_args()

    # Setup logging
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level="INFO")

    cleanup = ReportCleanup()

    if args.disk_usage:
        cleanup.print_disk_usage()
        return

    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be actually removed")
        logger.info(f"Would clean up reports older than {args.days} days")
        cleanup.print_disk_usage()
        return

    # Perform cleanup
    results = cleanup.cleanup_all(args.days)

    logger.info(f"Cleanup summary:")
    logger.info(f"  Old reports removed: {results['old_reports_cleaned']}")
    logger.info(f"  Empty directories removed: {results['empty_dirs_cleaned']}")


if __name__ == "__main__":
    main()
