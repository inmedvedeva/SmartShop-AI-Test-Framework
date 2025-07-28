"""
Performance monitoring utilities for SmartShop AI Test Framework
"""

import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import psutil
from loguru import logger

from src.core.constants import REPORT_DIR


@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""

    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    network_io: dict[str, float]


class PerformanceMonitor:
    """Performance monitoring class"""

    def __init__(self, interval: float = 1.0, report_dir: str = REPORT_DIR):
        self.interval = interval
        self.report_dir = report_dir
        self.monitoring = False
        self.metrics: list[PerformanceMetrics] = []
        self.monitor_thread: threading.Thread | None = None
        self.start_time: float | None = None
        self.end_time: float | None = None

    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring:
            logger.warning("Performance monitoring already started")
            return

        self.monitoring = True
        self.start_time = time.time()
        self.metrics.clear()

        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.monitoring:
            logger.warning("Performance monitoring not started")
            return

        self.monitoring = False
        self.end_time = time.time()

        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        logger.info("Performance monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics.append(metrics)
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in performance monitoring: {e}")
                break

    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_available_mb = memory.available / (1024 * 1024)

            # Disk usage
            disk = psutil.disk_usage("/")
            disk_usage_percent = disk.percent

            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv,
            }

            return PerformanceMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                memory_available_mb=memory_available_mb,
                disk_usage_percent=disk_usage_percent,
                network_io=network_io,
            )

        except Exception as e:
            logger.error(f"Failed to collect performance metrics: {e}")
            # Return empty metrics
            return PerformanceMetrics(
                timestamp=time.time(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                memory_available_mb=0.0,
                disk_usage_percent=0.0,
                network_io={},
            )

    def get_summary(self) -> dict:
        """Get performance summary"""
        if not self.metrics:
            return {}

        cpu_values = [m.cpu_percent for m in self.metrics]
        memory_values = [m.memory_percent for m in self.metrics]

        summary = {
            "monitoring_duration": (
                self.end_time - self.start_time if self.end_time else 0
            ),
            "samples_collected": len(self.metrics),
            "cpu": {
                "average": sum(cpu_values) / len(cpu_values),
                "max": max(cpu_values),
                "min": min(cpu_values),
            },
            "memory": {
                "average": sum(memory_values) / len(memory_values),
                "max": max(memory_values),
                "min": min(memory_values),
            },
            "peak_memory_used_mb": max(m.memory_used_mb for m in self.metrics),
            "peak_disk_usage": max(m.disk_usage_percent for m in self.metrics),
        }

        return summary

    def save_report(self, filename: str | None = None) -> str:
        """Save performance report"""
        if not self.metrics:
            logger.warning("No metrics to save")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"

        import json

        report_data = {
            "summary": self.get_summary(),
            "metrics": [
                {
                    "timestamp": m.timestamp,
                    "cpu_percent": m.cpu_percent,
                    "memory_percent": m.memory_percent,
                    "memory_used_mb": m.memory_used_mb,
                    "memory_available_mb": m.memory_available_mb,
                    "disk_usage_percent": m.disk_usage_percent,
                    "network_io": m.network_io,
                }
                for m in self.metrics
            ],
        }

        report_path = f"{self.report_dir}/{filename}"
        with open(report_path, "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"Performance report saved: {report_path}")
        return report_path

    def __enter__(self):
        """Context manager entry"""
        self.start_monitoring()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_monitoring()


class TestPerformanceMonitor:
    """Test-specific performance monitor"""

    def __init__(self, test_name: str):
        self.test_name = test_name
        self.monitor = PerformanceMonitor()
        self.start_time: float | None = None
        self.end_time: float | None = None

    def start_test(self):
        """Start monitoring for a test"""
        self.start_time = time.time()
        self.monitor.start_monitoring()
        logger.info(f"Performance monitoring started for test: {self.test_name}")

    def end_test(self):
        """End monitoring for a test"""
        self.end_time = time.time()
        self.monitor.stop_monitoring()
        logger.info(f"Performance monitoring ended for test: {self.test_name}")

    def get_test_summary(self) -> dict:
        """Get test performance summary"""
        summary = self.monitor.get_summary()
        summary["test_name"] = self.test_name
        summary["test_duration"] = (
            self.end_time - self.start_time if self.end_time else 0
        )
        return summary

    def save_test_report(self) -> str:
        """Save test performance report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_{self.test_name}_{timestamp}.json"
        return self.monitor.save_report(filename)


def get_performance_monitor(interval: float = 1.0) -> PerformanceMonitor:
    """Factory function to get performance monitor"""
    return PerformanceMonitor(interval)


def get_test_performance_monitor(test_name: str) -> TestPerformanceMonitor:
    """Factory function to get test performance monitor"""
    return TestPerformanceMonitor(test_name)
