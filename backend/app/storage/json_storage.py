# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import json
import os
from pathlib import Path
from typing import Any


class JSONStorage:
    """
    Simple file-based JSON storage for prototype.

    Stores leave requests and notifications in JSON files.
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialize storage with data directory.

        Args:
            data_dir: Directory to store JSON files (relative to backend root)
        """
        # Get the backend directory (parent of app)
        backend_dir = Path(__file__).parent.parent.parent
        self.data_dir = backend_dir / data_dir
        self.data_dir.mkdir(exist_ok=True)

        self.leave_requests_file = self.data_dir / "leave_requests.json"
        self.notifications_file = self.data_dir / "notifications.json"

        # Initialize files if they don't exist
        self._init_file(self.leave_requests_file, [])
        self._init_file(self.notifications_file, [])

    def _init_file(self, filepath: Path, default_data: Any):
        """Initialize a JSON file with default data if it doesn't exist."""
        if not filepath.exists():
            with open(filepath, 'w') as f:
                json.dump(default_data, f, indent=2, default=str)

    def _read_json(self, filepath: Path) -> Any:
        """Read JSON data from file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Return empty list if file is corrupted or missing
            return []

    def _write_json(self, filepath: Path, data: Any):
        """Write JSON data to file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    # Leave Request Operations

    def get_all_leave_requests(self) -> list[dict]:
        """Get all leave requests."""
        return self._read_json(self.leave_requests_file)

    def get_leave_request_by_id(self, request_id: str) -> dict | None:
        """Get a specific leave request by ID."""
        requests = self.get_all_leave_requests()
        for req in requests:
            if req.get("id") == request_id:
                return req
        return None

    def create_leave_request(self, request_data: dict) -> dict:
        """Create a new leave request."""
        requests = self.get_all_leave_requests()
        requests.append(request_data)
        self._write_json(self.leave_requests_file, requests)
        return request_data

    def update_leave_request(self, request_id: str, updates: dict) -> dict | None:
        """Update an existing leave request."""
        requests = self.get_all_leave_requests()
        for i, req in enumerate(requests):
            if req.get("id") == request_id:
                requests[i].update(updates)
                self._write_json(self.leave_requests_file, requests)
                return requests[i]
        return None

    def delete_leave_request(self, request_id: str) -> bool:
        """Delete a leave request."""
        requests = self.get_all_leave_requests()
        original_len = len(requests)
        requests = [req for req in requests if req.get("id") != request_id]

        if len(requests) < original_len:
            self._write_json(self.leave_requests_file, requests)
            return True
        return False

    # Notification Operations

    def get_all_notifications(self) -> list[dict]:
        """Get all notifications."""
        return self._read_json(self.notifications_file)

    def get_notifications_by_request_id(self, request_id: str) -> list[dict]:
        """Get all notifications for a specific leave request."""
        notifications = self.get_all_notifications()
        return [n for n in notifications if n.get("request_id") == request_id]

    def get_notification_by_id(self, notification_id: str) -> dict | None:
        """Get a specific notification by ID."""
        notifications = self.get_all_notifications()
        for notif in notifications:
            if notif.get("id") == notification_id:
                return notif
        return None

    def create_notification(self, notification_data: dict) -> dict:
        """Create a new notification."""
        notifications = self.get_all_notifications()
        notifications.append(notification_data)
        self._write_json(self.notifications_file, notifications)
        return notification_data

    def update_notification(self, notification_id: str, updates: dict) -> dict | None:
        """Update an existing notification."""
        notifications = self.get_all_notifications()
        for i, notif in enumerate(notifications):
            if notif.get("id") == notification_id:
                notifications[i].update(updates)
                self._write_json(self.notifications_file, notifications)
                return notifications[i]
        return None

    def delete_notification(self, notification_id: str) -> bool:
        """Delete a notification."""
        notifications = self.get_all_notifications()
        original_len = len(notifications)
        notifications = [n for n in notifications if n.get("id") != notification_id]

        if len(notifications) < original_len:
            self._write_json(self.notifications_file, notifications)
            return True
        return False

    def mark_notification_as_read(self, notification_id: str) -> dict | None:
        """Mark a notification as read."""
        return self.update_notification(notification_id, {"read_status": True})

    def mark_notification_as_unread(self, notification_id: str) -> dict | None:
        """Mark a notification as unread."""
        return self.update_notification(notification_id, {"read_status": False})
