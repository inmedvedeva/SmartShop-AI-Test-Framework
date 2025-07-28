"""
Monitoring utilities for SmartShop AI Test Framework
"""

import json
import threading
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from src.core.constants import REPORT_DIR


@dataclass
class TestEvent:
    """Test event data class"""

    timestamp: float
    event_type: str
    test_name: str
    status: str
    duration: float | None = None
    error_message: str | None = None
    metadata: dict[str, Any] | None = None


class TestMonitor:
    """Test monitoring class"""

    def __init__(self, report_dir: str = REPORT_DIR):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
        self.events: list[TestEvent] = []
        self.test_start_times: dict[str, float] = {}
        self.callbacks: list[Callable] = []
        self.monitoring = False

    def start_monitoring(self):
        """Start test monitoring"""
        self.monitoring = True
        self.events.clear()
        self.test_start_times.clear()
        logger.info("Test monitoring started")

    def stop_monitoring(self):
        """Stop test monitoring"""
        self.monitoring = False
        logger.info("Test monitoring stopped")

    def register_callback(self, callback: Callable[[TestEvent], None]):
        """Register callback for test events"""
        self.callbacks.append(callback)
        logger.info("Test event callback registered")

    def _notify_callbacks(self, event: TestEvent):
        """Notify all registered callbacks"""
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in test event callback: {e}")

    def test_started(self, test_name: str, metadata: dict[str, Any] | None = None):
        """Record test start event"""
        if not self.monitoring:
            return

        timestamp = time.time()
        self.test_start_times[test_name] = timestamp

        event = TestEvent(
            timestamp=timestamp,
            event_type="test_started",
            test_name=test_name,
            status="started",
            metadata=metadata,
        )

        self.events.append(event)
        self._notify_callbacks(event)
        logger.info(f"Test started: {test_name}")

    def test_passed(self, test_name: str, metadata: dict[str, Any] | None = None):
        """Record test pass event"""
        if not self.monitoring:
            return

        timestamp = time.time()
        start_time = self.test_start_times.get(test_name, timestamp)
        duration = timestamp - start_time

        event = TestEvent(
            timestamp=timestamp,
            event_type="test_passed",
            test_name=test_name,
            status="passed",
            duration=duration,
            metadata=metadata,
        )

        self.events.append(event)
        self._notify_callbacks(event)
        logger.info(f"Test passed: {test_name} (duration: {duration:.2f}s)")

    def test_failed(
        self,
        test_name: str,
        error_message: str,
        metadata: dict[str, Any] | None = None,
    ):
        """Record test failure event"""
        if not self.monitoring:
            return

        timestamp = time.time()
        start_time = self.test_start_times.get(test_name, timestamp)
        duration = timestamp - start_time

        event = TestEvent(
            timestamp=timestamp,
            event_type="test_failed",
            test_name=test_name,
            status="failed",
            duration=duration,
            error_message=error_message,
            metadata=metadata,
        )

        self.events.append(event)
        self._notify_callbacks(event)
        logger.error(
            f"Test failed: {test_name} (duration: {duration:.2f}s) - {error_message}"
        )

    def test_skipped(
        self,
        test_name: str,
        reason: str = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Record test skip event"""
        if not self.monitoring:
            return

        timestamp = time.time()
        start_time = self.test_start_times.get(test_name, timestamp)
        duration = timestamp - start_time

        event = TestEvent(
            timestamp=timestamp,
            event_type="test_skipped",
            test_name=test_name,
            status="skipped",
            duration=duration,
            error_message=reason,
            metadata=metadata,
        )

        self.events.append(event)
        self._notify_callbacks(event)
        logger.warning(f"Test skipped: {test_name} - {reason}")

    def get_test_summary(self) -> dict[str, Any]:
        """Get test execution summary"""
        if not self.events:
            return {}

        passed = sum(1 for e in self.events if e.event_type == "test_passed")
        failed = sum(1 for e in self.events if e.event_type == "test_failed")
        skipped = sum(1 for e in self.events if e.event_type == "test_skipped")
        total = passed + failed + skipped

        durations = [e.duration for e in self.events if e.duration is not None]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "average_duration": avg_duration,
            "total_duration": sum(durations) if durations else 0,
        }

    def save_report(self, filename: str | None = None) -> str:
        """Save test monitoring report"""
        if not self.events:
            logger.warning("No test events to save")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_monitoring_report_{timestamp}.json"

        report_data = {
            "summary": self.get_test_summary(),
            "events": [asdict(event) for event in self.events],
            "monitoring_start": (
                min(e.timestamp for e in self.events) if self.events else 0
            ),
            "monitoring_end": (
                max(e.timestamp for e in self.events) if self.events else 0
            ),
        }

        report_path = self.report_dir / filename
        with open(report_path, "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"Test monitoring report saved: {report_path}")
        return str(report_path)


class MetricsCollector:
    """Metrics collection class"""

    def __init__(self, report_dir: str = REPORT_DIR):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
        self.metrics: dict[str, list[dict[str, Any]]] = {}
        self.collecting = False

    def start_collecting(self):
        """Start metrics collection"""
        self.collecting = True
        self.metrics.clear()
        logger.info("Metrics collection started")

    def stop_collecting(self):
        """Stop metrics collection"""
        self.collecting = False
        logger.info("Metrics collection stopped")

    def add_metric(self, metric_name: str, value: Any, timestamp: float | None = None):
        """Add a metric value"""
        if not self.collecting:
            return

        if timestamp is None:
            timestamp = time.time()

        if metric_name not in self.metrics:
            self.metrics[metric_name] = []

        self.metrics[metric_name].append({"timestamp": timestamp, "value": value})

    def get_metric_summary(self, metric_name: str) -> dict[str, Any]:
        """Get summary for a specific metric"""
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return {}

        values = [m["value"] for m in self.metrics[metric_name]]

        # Handle numeric values
        if all(isinstance(v, (int, float)) for v in values):
            return {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "average": sum(values) / len(values),
                "latest": values[-1],
            }
        else:
            return {
                "count": len(values),
                "latest": values[-1],
                "unique_values": list(set(values)),
            }

    def save_metrics(self, filename: str | None = None) -> str:
        """Save collected metrics"""
        if not self.metrics:
            logger.warning("No metrics to save")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_report_{timestamp}.json"

        report_data = {
            "collection_start": (
                min(
                    min(m["timestamp"] for m in metric_list)
                    for metric_list in self.metrics.values()
                    if metric_list
                )
                if self.metrics
                else 0
            ),
            "collection_end": (
                max(
                    max(m["timestamp"] for m in metric_list)
                    for metric_list in self.metrics.values()
                    if metric_list
                )
                if self.metrics
                else 0
            ),
            "metrics": {
                name: {"data": data, "summary": self.get_metric_summary(name)}
                for name, data in self.metrics.items()
            },
        }

        report_path = self.report_dir / filename
        with open(report_path, "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"Metrics report saved: {report_path}")
        return str(report_path)


def get_test_monitor() -> TestMonitor:
    """Factory function to get test monitor"""
    return TestMonitor()


def get_metrics_collector() -> MetricsCollector:
    """Factory function to get metrics collector"""
    return MetricsCollector()
